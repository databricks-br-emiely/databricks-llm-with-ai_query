# Databricks notebook source
# MAGIC %md
# MAGIC # 3/ Revisão e classificação automatizada de produtos com funções SQL
# MAGIC
# MAGIC
# MAGIC Nesta demonstração, exploraremos a função SQL AI `AI_QUERY` para criar um pipeline extraindo informações de avaliação do produto.
# MAGIC
# MAGIC <img src="https://github.com/anasanchezss9/databricks_sql_e_openai/blob/main/images/sql-ai-function-flow.png?raw=true" width="1000">
# MAGIC
# MAGIC <!-- Collect usage data (view). Remove it to disable collection. View README for more details.  -->
# MAGIC <img width="1px" src="https://www.google-analytics.com/collect?v=1&gtm=GTM-NKQ8TT7&tid=UA-163989034-1&aip=1&t=event&ec=dbdemos&ea=VIEW&dp=%2F_dbdemos%2FDBSQL%2Fsql-ai-functions%2F04-automated-product-review-and-answer&cid=984752964297111&uid=7582903553287639">

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Simplificando o acesso à função de IA para usuários SQL
# MAGIC
# MAGIC Como lembrete, a assinatura `AI_QUERY` é a seguinte:
# MAGIC
# MAGIC ```
# MAGIC SELECT AI_QUERY(<Prompt a ser enviado ao modelo>,
# MAGIC                 <Nome do modelo implantado em "Serving" (modelo customizado, foundation ou externo)>)
# MAGIC ```
# MAGIC
# MAGIC No [notebook anterior]($./03-Generate-fake-data-with-AI-functions), criamos uma função wrapper `ask_llm` para simplificar nossa operação SQL e ocultar os detalhes de configuração para os usuários finais. Reutilizaremos esta função para este pipeline.
# MAGIC
# MAGIC <img src="https://github.com/anasanchezss9/databricks_sql_e_openai/blob/main/images/sql-ai-function-review-wrapper.png?raw=true" width=" 1200 pixels">
# MAGIC
# MAGIC Para simplificar a experiência do usuário para nossos analistas, construiremos funções SQL prescritivas que fazem perguntas em linguagem natural sobre nossos dados e retornam as respostas como dados estruturados.

# COMMAND ----------

# MAGIC %run "./_resources/Classroom-Setup"

# COMMAND ----------

catalog = "workshops_databricks"
db=f"llms_managed_{username}"

endpoint_name= 'databricks-dbrx-instruct'
#### Preencha com o nome do seu warehouse
warehouse_name="ana-warehouse-preview"

# COMMAND ----------

# MAGIC %run ./_resources/00-init $catalog=catalog $db=db

# COMMAND ----------

# DBTITLE 1,Review our raw data
#See companion notebook
sql_api = SQLStatementAPI(warehouse_name = warehouse_name, catalog = catalog, schema = db)

display(sql_api.execute_sql("""SELECT * FROM avaliacoes_fake INNER JOIN clientes_fake using (id_cliente)"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Revise a análise com a engenharia de prompt do modelo
# MAGIC &nbsp;
# MAGIC Os segredos para obter resultados úteis de um modelo Mixtral-8x7B são:
# MAGIC - Fazer um pedido bem formulado
# MAGIC - Ser específico sobre o tipo de resposta que você espera
# MAGIC
# MAGIC Para obter resultados em um formato que possamos armazenar facilmente em uma tabela, pediremos ao modelo para retornar o resultado em uma string que reflita a representação `JSON` e seja muito específico quanto ao esquema que esperamos
# MAGIC
# MAGIC Aqui está o prompt que desenvolvemos:
# MAGIC ```
# MAGIC Um cliente deixou um comentário sobre um produto. Queremos acompanhar qualquer pessoa que pareça infeliz.
# MAGIC Extraia todas as entidades mencionadas. Para cada entidade:
# MAGIC - classificar o sentimento como ["positivo","neutro","negativo"]
# MAGIC - se o cliente requer acompanhamento: S ou N
# MAGIC - motivo para exigir acompanhamento
# MAGIC
# MAGIC Retorne SOMENTE JSON. Nenhum outro texto fora do JSON. Formato JSON:
# MAGIC [{
# MAGIC      "nome_do_produto": <nome do produto>,
# MAGIC      "sentiment": <revisar sentimento, um de ["positivo","neutro","negativo"]>,
# MAGIC      "acompanhamento": <S ou N para acompanhamento>,
# MAGIC      "motivo_acompanhamento": <motivo do acompanhamento>
# MAGIC }]
# MAGIC
# MAGIC Avaliação:
# MAGIC <insira o texto da avaliação aqui>
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,Create the ANNOTATE function
sql_api.execute_sql("""
    CREATE OR REPLACE FUNCTION enriquecer_avaliacao(avaliacao STRING)
    RETURNS STRUCT<tipodoproduto: STRING, sentimento: STRING, acompanhamento: STRING, motivoacompanhamento: STRING>
    RETURN FROM_JSON(
      ASK_LLM(CONCAT(
      'Um cliente deixou um comentário. Acompanhamos qualquer pessoa que pareça infeliz.
          extraia as seguintes informações:
           - classificar o sentimento como ["positivo","neutro","negativo"]
           - retornar se o cliente requer acompanhamento: S ou N
           - se for necessário acompanhamento, explique qual é o motivo principal

       Dê-me apenas JSON. Nenhum texto fora do JSON. Sem adicionar: ```json  no retorno:
          {
          "tipodoproduto": <nome do produto>,
          "sentimento": <revisar sentimento, um de ["positivo","neutro","negativo"]>,
          "acompanhamento": <S ou N para acompanhamento>,
          "motivoacompanhamento": <motivo do acompanhamento>
          }

          Nunca retorne null.
        
         avaliacao:', avaliacao)),
      "STRUCT<tipodoproduto: STRING, sentimento: STRING, acompanhamento: STRING, motivoacompanhamento: STRING>")""")

# COMMAND ----------

sql_api.execute_sql("""
  CREATE OR REPLACE TABLE avaliacoes_enriquecidas as 
    SELECT * EXCEPT (avaliacoes_enriquecidas), avaliacoes_enriquecidas.* FROM (
      SELECT *, enriquecer_avaliacao(avaliacao) AS avaliacoes_enriquecidas
        FROM avaliacoes_fake LIMIT 10)
    INNER JOIN clientes_fake using (id_cliente)
    """)


# COMMAND ----------

# DBTITLE 1,Extract information from all our reviews
display(sql_api.execute_sql("""SELECT * FROM avaliacoes_enriquecidas"""))

# COMMAND ----------

# Generate a response to a customer based on their complaint
sql_api.execute_sql("""
  CREATE OR REPLACE FUNCTION GERE_RESPOSTAS(nome STRING, sobrenome STRING, qnt_produtos INT, produto STRING, motivo STRING)
  RETURNS STRING
  RETURN ask_llm(
    CONCAT("Nosso cliente se chama ", nome, " ", sobrenome, "quem utilizou", qnt_produtos, "serviços do banco esse ano ficaram insatisfeitos com", produto,
     "especificamente devido a", motivo, ". Forneça uma mensagem empática em português do Brasil que eu possa enviar ao meu cliente
     incluindo a oferta de uma ligação com o gerente de produto relevante para deixar comentários. Eu quero reconquistar meu cliente e não quero aconteça o churn.")
  )""")



# COMMAND ----------

# Let's test our response
r = sql_api.execute_sql("""SELECT GERE_RESPOSTAS("Ana", "Silva", 235, "cartão de crédito", "teve seu cartão negado durante uma compra na black friday") AS resposta_cliente""")
display_answer(r.iloc[0]['resposta_cliente'])

# COMMAND ----------

sql_api.execute_sql("""
  CREATE OR REPLACE TABLE respostas_avaliacoes as 
    SELECT *,
      GERE_RESPOSTAS(nome, sobrenome, qnt_pedido, tipodoproduto, motivoacompanhamento) AS rascunho_resposta
    FROM avaliacoes_enriquecidas where acompanhamento='S'
    LIMIT 10""")

# COMMAND ----------

display(sql_api.execute_sql("""SELECT * FROM respostas_avaliacoes"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximos passos
# MAGIC Além da função AI Query, temos diversas outras funções de AI no Databricks para atender demandas específicas! Abra [04- Extra: Outras Funções de AI
# MAGIC ]($./04-Funções-de-IA-do-Databricks) para continuar.
# MAGIC
# MAGIC
# MAGIC Volte para [a introdução]($./README.md)

# COMMAND ----------



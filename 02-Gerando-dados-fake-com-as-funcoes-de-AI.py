# Databricks notebook source
# MAGIC %md
# MAGIC # 2/ Introdução à função SQL AI: gerando dados fake com APIs LLMs hospedados no Databricks (Foundation Models)
# MAGIC
# MAGIC Para esta demonstração, começaremos gerando dados fake usando `AI_QUERY()`.
# MAGIC
# MAGIC Os dados de amostra simularão as avaliações dos clientes sobre produtos bancários.
# MAGIC
# MAGIC ## Trabalhando com a função `AI_QUERY`
# MAGIC
# MAGIC Nossa assinatura de função é a seguinte:
# MAGIC
# MAGIC ```
# MAGIC SELECT AI_QUERY(<Prompt a ser enviado ao modelo>,
# MAGIC                 <Nome do modelo implantado em "Serving" (modelo customizado, foundation ou externo)>)
# MAGIC ```
# MAGIC
# MAGIC `AI_QUERY` enviará o prompt para o modelo remoto configurado e recuperará o resultado como SQL.
# MAGIC
# MAGIC Vamos ver como usá-lo.
# MAGIC
# MAGIC <!-- Colete dados de uso (visualização). Remova-o para desativar a coleta. Veja o README para mais detalhes. -->
# MAGIC <img width="1px" src="https://www.google-analytics.com/collect?v=1&gtm=GTM-NKQ8TT7&tid=UA-163989034-1&aip=1&t=event&ec=dbdemos&ea=VIEW&dp=%2F_dbdemos%2FDBSQL %2Fsql-ai-functions%2F03-Generate-fake-data-with-AI-functions&cid=984752964297111&uid=7582903553287639">

# COMMAND ----------

# MAGIC %run "./_resources/Classroom-Setup"

# COMMAND ----------

catalog = "workshops_databricks"
db=f"llms_managed_{username}"

# COMMAND ----------

# MAGIC %run ./_resources/00-init $catalog=catalog $db=db

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Nossa primeira função SQL de AI
# MAGIC
# MAGIC Vamos rodar uma função SQL de AI simples. Pediremos ao modelo que gere um texto para uma análise de produto de bancário.
# MAGIC
# MAGIC *Observe que, por enquanto, as funções SQL AI só funcionarão em um **Databricks SQL Pro ou Serverless warehouse** e **não** em um Notebook usando cluster interativo.*
# MAGIC
# MAGIC Para facilitar a navegação nesta demonstração, usaremos Databricks [SQL Statement API](https://docs.databricks.com/api-explorer/workspace/statementexecution/executestatement) para enviar nossas consultas SQL para um endpoint SQL Serverless que criamos para você com esta demonstração.
# MAGIC
# MAGIC *(Como alternativa, você pode copiar/colar o código SQL de uma nova consulta usando o [Databricks SQL Editor](/sql/editor/) para vê-lo em ação)*

# COMMAND ----------

endpoint_name= 'databricks-dbrx-instruct'
#### Preencha com o nome do seu warehouse
warehouse_name="ana-warehouse-preview"

# COMMAND ----------

#See companion notebook
sql_api = SQLStatementAPI(warehouse_name =warehouse_name , catalog = catalog, schema = db)

df = sql_api.execute_sql(f"""
SELECT ai_query('{endpoint_name}', 
  "Gere uma breve amostra de review de um cartão de crédito em português do Brasil. O cliente que escreveu o review está muito insatisfeito com o produto por causa de uma situação que foi utiliza-lo durante a black friday e seu cartão foi bloqueado e não conseguiu realizar a compra.") as product_review""")
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Adicionando uma função wrapper para simplificar a chamada
# MAGIC
# MAGIC Ter que especificar todos os nossos parâmetros pode ser difícil de usar, especialmente para analistas de dados, que devem se concentrar na elaboração de prompts adequados e não no gerenciamento de credenciais.
# MAGIC
# MAGIC Para simplificar as próximas etapas de nossa demonstração, criaremos uma função SQL wrapper `ASK_LLM` com uma string como parâmetro de entrada (a pergunta a ser feita) e empacotaremos toda a configuração do modelo dentro da função.
# MAGIC
# MAGIC <img src="https://github.com/anasanchezss9/databricks_sql_e_openai/blob/main/images/sql-ai-function-review-wrapper.png?raw=true" width="1200px">

# COMMAND ----------

# DBTITLE 1,SQL admin setup wrapper function
sql_api.execute_sql(f"""CREATE OR REPLACE FUNCTION ASK_LLM(prompt STRING)
                                RETURNS STRING
                                RETURN 
                                  ai_query('{endpoint_name}', prompt)""")

# COMMAND ----------

# DBTITLE 1,SQL Analyst simply use the wrapper
display(sql_api.execute_sql("""SELECT ASK_LLM("Gere uma breve review do produto em português do brasil para um cartão de crédito. O cliente que escreveu o review está muito satisfeito com o produto.") as avaliacao"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Gerando um conjunto de dados de amostra mais completo com engenharia de prompt
# MAGIC
# MAGIC Agora que sabemos como enviar uma consulta básica ao modelo usando funções SQL, vamos fazer um pedido mais detalhada ao modelo.
# MAGIC
# MAGIC Pediremos diretamente ao modelo para gerar várias linhas e retornar diretamente como um json.
# MAGIC
# MAGIC Aqui está um exemplo rápido para gerar JSON:
# MAGIC ```
# MAGIC Gere um conjunto de dados de amostra de 2 linhas que contenha as seguintes colunas: "data" (datas aleatórias em 2022),
# MAGIC "review_id" (id aleatório), "id_cliente" (aleatório de 1 a 100) e "review". As avaliações devem imitar análises úteis de produtos
# MAGIC deixado em um site de um banco, eles tem diversos produtos, tais como: cartão de crédito; seguro de residencia, carro, celular; finciamento; empréstimo; conta corrente; entre outros.
# MAGIC       
# MAGIC As avaliações devem ser sobre os produtos bancários
# MAGIC
# MAGIC As revisões devem variar em extensão (menor: uma frase, mais longa: 2 parágrafos), sentimento e complexidade. Uma revisão muito complexa falaria sobre vários tópicos (entidades) sobre o produto com sentimentos variados por tópico. Forneça uma mistura de aspectos positivos, negativos, e comentários neutros.
# MAGIC
# MAGIC Dê-me apenas JSON. Nenhum texto fora do JSON. Sem explicações ou notas
# MAGIC [{"review_date":<date>, "review_id":<long>, "id_cliente":<long>, "review":<string>}]
# MAGIC ```

# COMMAND ----------

fake_reviews = sql_api.execute_sql("""
SELECT ASK_LLM(
      'Gere um conjunto de dados de amostra de 2 linhas que contenha as seguintes colunas: "data" (datas aleatórias em 2022),
       "review_id" (id aleatório), "id_cliente" (aleatório de 1 a 100) e "review". As avaliações devem imitar análises úteis de produtos
       deixado em um site de um banco, eles tem diversos produtos, tais como: cartão de crédito; seguro de residencia, carro, celular; finciamento; empréstimo e conta corrente.
      
       As avaliações devem ser sobre os produtos bancários e em português do Brasil.

       As revisões devem variar em extensão (menor: uma frase, mais longa: 2 parágrafos), sentimento e complexidade. Uma revisão muito complexa falaria sobre vários tópicos (entidades) sobre o produto com sentimentos variados por tópico. Forneça uma mistura de aspectos positivos, negativos, e comentários neutros.

       Dê-me apenas JSON. Nenhum texto fora do JSON. Sem adicionar: ```json  no retorno.
      [{"review_date":<date>, "review_id":<long>, "id_cliente":<long>, "review":<string>}]') as reviews""")
display(fake_reviews)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Convertendo os resultados de json para dataframe
# MAGIC
# MAGIC Nossos resultados parecem bons. Tudo o que precisamos fazer agora é transformar os resultados do texto em JSON e explodir os resultados em N linhas de um dataframe.
# MAGIC
# MAGIC Vamos criar uma nova função para fazer isso:

# COMMAND ----------

fake_reviews = sql_api.execute_sql("""
CREATE OR REPLACE FUNCTION GERE_AVALIACOES_fake(num_reviews INT DEFAULT 5)
RETURNS array<struct<data_avaliacao:date, id_avaliacao:long, id_cliente:long, avaliacao:string>>
RETURN 
SELECT FROM_JSON(
    ASK_LLM(
    CONCAT('Gere um conjunto de dados de amostra de ', num_reviews, ' linhas que contém as seguintes colunas: "data" (datas aleatórias em 2022),
       "id_avaliacao" (id aleatório), "id_cliente" (valor unico de 1 a 15) e "review". As avaliações devem imitar análises úteis de produtos
       deixado em um site de um banco, eles tem diversos produtos, tais como: cartão de crédito; seguro de residencia, carro, celular; finciamento; empréstimo e conta corrente.
      
       As avaliações devem ser sobre os produtos bancários.

       As avaliações devem variar em extensão (menor: uma frase, mais longa: 4 parágrafos), sentimento e complexidade. Uma avaliação muito complexa
       falaria sobre vários tópicos (entidades) sobre o produto com sentimentos variados por tópico. Forneça uma mistura de aspectos positivos, negativos,
       e comentários neutros.


       Dê-me apenas JSON. Nenhum texto fora do JSON. Sem adicionar: ```json  no retorno.
       [{"data_avaliacao":<date>, "id_avaliacao":<long>, "id_cliente":<long>, "avaliacao":<string>}]')), 
      "array<struct<data_avaliacao:date, id_avaliacao:long, id_cliente:long, avaliacao:string>>")""")

# COMMAND ----------

# DBTITLE 1,Explode the json result as a table
display(sql_api.execute_sql("""SELECT review.* FROM (
                                SELECT explode(reviews) as review FROM (
                                  SELECT GERE_AVALIACOES_fake(10) as reviews))"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Salvando nosso conjunto de dados como uma tabela para ser usada diretamente em nossa demonstração.
# MAGIC
# MAGIC *Observe que se quiser criar mais linhas, você pode primeiro criar uma tabela e adicionar várias linhas, com informações extras que você pode concatenar ao seu prompt, como categorias, satisfação esperada do cliente, etc. Depois que sua tabela for criada, você poderá chamar uma nova função GENERATE personalizada, pegando mais parâmetros e criando um prompt mais avançado**

# COMMAND ----------

# DBTITLE 1,Save the crafted review as a new table
sql_api.execute_sql(f"""
CREATE OR REPLACE TABLE avaliacoes_fake
COMMENT "Dados brutos de avaliacoes fake"
AS
SELECT review.* FROM (
  SELECT explode(reviews) as review FROM (
    SELECT GERE_AVALIACOES_fake(10) as reviews))""")

# COMMAND ----------

display(spark.sql(f"select * from {catalog}.{db}.avaliacoes_fake"))

# COMMAND ----------

# DBTITLE 1,Além disso, vamos gerar alguns usuários utilizando a mesma ideia:
fake_reviews = sql_api.execute_sql("""
CREATE OR REPLACE FUNCTION GERE_CLIENTES_fake(num_reviews INT DEFAULT 10)
RETURNS array<struct<id_cliente:long, nome:string, sobrenome:string, qnt_pedido:int>>
RETURN 
SELECT FROM_JSON(
    ASK_LLM(
      CONCAT('Gere um conjunto de dados de amostra de clientes brasileiros ', num_reviews,' contendo as seguintes colunas:
       "id_cliente" (long from 1 to ', num_reviews, '), "nome", "sobrenome" e qnt_pedido (número positivo aleatório, menor que 200)

       Dê-me apenas JSON. Nenhum texto fora do JSON. Sem adicionar: ```json  no retorno.
      [{"id_cliente":<long>, "nome":<string>, "sobrenome":<string>, "qnt_pedido":<int>}]')), 
      "array<struct<id_cliente:long, nome:string, sobrenome:string, qnt_pedido:int>>")""")

sql_api.execute_sql("""
CREATE OR REPLACE TABLE clientes_fake
COMMENT "Raw customers"
AS
SELECT customer.* FROM (
  SELECT explode(customers) as customer FROM (
    SELECT GERE_CLIENTES_FAKE(10) as customers))""")



# COMMAND ----------

display(spark.sql(f"select * from {catalog}.{db}.clientes_fake"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próximos passos
# MAGIC Agora estamos prontos para implementar nosso pipeline para extrair informações de nossas análises! Abra [03-revisão e resposta automatizada de produto]($./03-automatizando-as-avaliacoes-e-respostas) para continuar.
# MAGIC
# MAGIC
# MAGIC Volte para [a introdução]($./README.md)

# COMMAND ----------



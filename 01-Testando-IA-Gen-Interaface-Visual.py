# Databricks notebook source
# MAGIC %md
# MAGIC #1/ APIs de foundation model do Databricks
# MAGIC
# MAGIC ## Databricks Model Serving
# MAGIC
# MAGIC Com o Databricks Model serving é possível realizar o gerenciamento unificado de todos os modelos que você precisa servir. Ele oferece uma interface unificada para gerenciar e integrar modelos de IA via API REST, adequando-se a aplicações web e clients. Com alta disponibilidade e baixa latência, o serviço ajusta automaticamente a escala de recursos para atender à demanda variável, utilizando computação sem servidor para eficiência de custos. Os usuários podem implantar modelos personalizados, modelos abertos de ponta com suporte para inferência otimizada e modelos externos, com controles centralizados e gestão de acesso
# MAGIC
# MAGIC <img src="https://github.com/anasanchezss9/databricks_sql_e_openai/blob/main/images/model-serving.png?raw=true" width="1200">
# MAGIC
# MAGIC
# MAGIC
# MAGIC ## O que são as APIs de foundation model do Databricks?
# MAGIC O Serviço de Modelo do Databricks agora dá suporte a APIs de Modelo de Fundação que permitem acessar e consultar modelos abertos de última geração de um ponto de extremidade de serviço. Com as APIs do Modelo Base, você pode criar aplicativos de maneira rápida e fácil que aproveitam um modelo de IA generativa de alta qualidade sem manter uma implantação de modelo própria.
# MAGIC
# MAGIC ### Usar APIs de foundation model
# MAGIC
# MAGIC Esses modelos são acessíveis no workspace do Azure Databricks. Para acessá-los em seu workspace, navegue até a guia <img src="https://github.com/anasanchezss9/databricks_sql_e_openai/blob/main/images/serving menu.png?raw=true" width="160"> na barra lateral esquerda. As APIs de foundation model estão localizadas na parte superior da exibição de lista de endpoints.
# MAGIC
# MAGIC <img src="https://learn.microsoft.com/pt-br/azure/databricks/_static/images/machine-learning/serving-endpoints-list.png" width="1200">
# MAGIC
# MAGIC
# MAGIC Para saber os modelos presentes, confira a documentação para ter a informação mais atualizada: [Modelos suportados](https://learn.microsoft.com/pt-br/azure/databricks/machine-learning/foundation-models/supported-models)
# MAGIC
# MAGIC
# MAGIC ### Testar as APIs de Foundation Models
# MAGIC
# MAGIC Para testar um dos modelos, você pode simplesmente clicar em **Query** e para perguntar o que é Databricks e obter a resposta em português basta colar o seguint promt no campo **Request**:
# MAGIC
# MAGIC ```json
# MAGIC {
# MAGIC   "messages": [
# MAGIC     {
# MAGIC       "role": "user",
# MAGIC       "content": "Me explique o que é Databricks, em português?"
# MAGIC     }
# MAGIC   ],
# MAGIC   "max_tokens": 128
# MAGIC }
# MAGIC ```
# MAGIC
# MAGIC <img src="https://github.com/anasanchezss9/databricks_sql_e_openai/blob/main/images/query-endpoint.png?raw=true" width="1200">
# MAGIC
# MAGIC
# MAGIC ## Playgroud
# MAGIC
# MAGIC Você pode interagir com modelos LLMs que estão servidos no Databricks (customizados, foundation ou externos) através do Playground de IA. O Playground de IA é um ambiente semelhante ao chat em que você pode testar e comparar LLMs. 
# MAGIC
# MAGIC
# MAGIC ### Testar as APIs de Foundation Models pelo Playgroud
# MAGIC
# MAGIC Para usar o AI Playground:
# MAGIC
# MAGIC 1. Selecione Playground no painel de navegação esquerdo em Machine Learning.
# MAGIC
# MAGIC 3. Selecione o modelo com o qual deseja interagir usando a lista dropdown no canto superior esquerdo.
# MAGIC
# MAGIC 4. Você pode fazer o seguinte:
# MAGIC
# MAGIC 5. Digite sua pergunta ou solicitação.
# MAGIC
# MAGIC 6. Selecione um exemplo de instrução de IA dentre as listadas na janela.
# MAGIC
# MAGIC 7. Você pode selecionar + para adicionar um endpoint. Isso permite comparar múltiplas respostas de modelos lado a lado.
# MAGIC
# MAGIC <img src="https://learn.microsoft.com/pt-br/azure/databricks/_static/images/machine-learning/ai-playground.gif" width="1200">
# MAGIC
# MAGIC
# MAGIC ## Referências
# MAGIC
# MAGIC | Documentação      | Link                                                                                       |
# MAGIC |-------------------|--------------------------------------------------------------------------------------------|
# MAGIC | Model Serving     | https://learn.microsoft.com/pt-pt/azure/databricks/machine-learning/model-serving/             |
# MAGIC | Foundation Models | https://learn.microsoft.com/pt-pt/azure/databricks/machine-learning/foundation-models/     |
# MAGIC | AI Playground     | https://learn.microsoft.com/pt-pt/azure/databricks/large-language-models/ai-playground |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Próxima etapa: gerar nosso conjunto de dados de demonstração aproveitando as funções de IA
# MAGIC
# MAGIC Abra o próximo Notebook para gerar alguns dados de amostra para nossa demonstração: [03-Gerando-dados-fake-com-as-funcoes-de-AI]($./02-Gerando-dados-fake-com-as-funcoes-de-AI)
# MAGIC
# MAGIC Volte para [a introdução]($./README.md)

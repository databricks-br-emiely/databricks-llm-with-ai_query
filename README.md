# Utilizando LLMs em suas queries com as funções de AI do Databricks

&nbsp;
## Utilize modelos LLMs a partir dos dados do Lakehouse usando AI_QUERY()

Este passo a passo mostra como usar os modelos servidos no Databricks (customizados, foundation e externos) com Databricks SQL AI Functions para processar dados não estruturados, identificar tópicos, sentimentos e gerar respostas.

As funções de IA simplificam a obtenção de significado de dados não estruturados e facilitam a interação dos analistas com LLMs usando SQL

Nesta demonstração, mostraremos como classificar e responder automaticamente às avaliações dos clientes, pedindo ao modelos de LLMpara detectar avaliações negativas e preparar uma resposta.

Também exploraremos como o LLM pode ser usado para gerar dados fakes.

&nbsp;
## Demo: Enriquecendo avaliações de clientes em escala com funções SQL AI do Databricks + LLM Fondation Model: Mixtral-8x7B

As funções AI são funções SQL integradas do Databricks, permitindo que você acesse Large Language Models (LLMs) diretamente do SQL.

LLMs populares, como o Mixtral-8x7B, permitem aplicar todos os tipos de transformações no texto, desde classificação, extração de informações até respostas automáticas.

Aproveitando as funções SQL AI do Databricks `AI_QUERY()`, agora você pode aplicar essas transformações e experimentar LLMs em seus dados a partir de uma interface SQL familiar.

Depois de desenvolver o prompt LLM correto, você pode transformá-lo rapidamente em um pipeline de produção usando ferramentas existentes do Databricks, como Delta Live Tables ou jobs agendados. Isso simplifica muito o fluxo de trabalho de desenvolvimento e produção para LLMs.

O AI Functions abstrai as complexidades técnicas de chamada de LLMs, permitindo que analistas e cientistas de dados comecem a usar esses modelos sem se preocupar com a infraestrutura subjacente.

### Aumentando a satisfação do cliente e redução de churn com análise automática de avaliações

Nesta demonstração, construiremos um pipeline de dados que recebe avaliações de clientes, na forma de texto de formato livre, e as enriquece com significado derivado de perguntas em linguagem natural do modelo Mixtral-8x7B. Forneceremos até recomendações sobre as próximas melhores ações para nossa equipe de atendimento ao cliente - ou seja, se um cliente precisa de acompanhamento e um exemplo de mensagem para acompanhamento

Para cada revisão, nós:
- Determine o sentimento e se uma resposta é necessária para o cliente
- Gerar uma resposta mencionando produtos alternativos que possam satisfazer o cliente


&nbsp;
<img src="https://github.com/anasanchezss9/databricks_sql_e_openai/blob/main/images/sql-ai-function-review.png?raw=true" width="1200">

<!-- Collect usage data (view). Remove it to disable collection. View README for more details.  -->
<img width="1px" src="https://www.google-analytics.com/collect?v=1&gtm=GTM-NKQ8TT7&tid=UA-163989034-1&aip=1&t=event&ec=dbdemos&ea=VIEW&dp=%2F_dbdemos%2FDBSQL%2Fsql-ai-functions%2F01-SQL-AI-Functions-Introduction&cid=984752964297111&uid=7582903553287639">


#### 0/ Configuração: obtenha sua configuração da API do Mixtral

##### Pré-requisitos

Para executar esta demonstração em seu próprio ambiente, você precisará atender a estes pré-requisitos:

- Acesso a um [warehouse Databricks SQL Pro ou Serverless](https://learn.microsoft.com/pt-br/azure/databricks/compute/sql-warehouse/create-sql-warehouse)
- Seu workspace Databricks deve estar em alguma região que já tenha sido lançado as APIs de foundation model:
  - [Requisitos de região das APIs de foundation model no Azure Databricks](https://learn.microsoft.com/pt-br/azure/databricks/machine-learning/foundation-models/#--requirements)
  - [Requisitos de região das APIs de foundation model no Databricks na AWS](https://docs.databricks.com/pt/machine-learning/foundation-models/index.html)


#### 1/ Testando as APIs de Fondation Models através das interfaces visuais

Para realizar testes nas APIs de Fondation Models em interface visual, podemos fazer de algumas formas:
- No menu lateral esquerdo do Databricks, abaixo de **Machine Learning**, podemos acessá-lo através do menu: <img src="https://github.com/anasanchezss9/databricks_sql_e_openai/blob/main/images/serving menu.png?raw=true" width="160">
- No menu lateral esquerdo do Databricks, abaixo de **Machine Learning**, podemos acessá-lo através do menu: <img src="https://github.com/anasanchezss9/databricks_sql_e_openai/blob/main/images/playgroung menu.png?raw=true" width="160">

Abra [02-Testando-IA-Gen-Interaface-Visual]($./01-Testando-IA-Gen-Interaface-Visual) para começar a testar um modelo de IA generativa através das interfaces visuais do Databricks!


#### 2/ Introdução ao `AI_QUERY`: Gerando dados falsos para nossa demonstração com Open AI

Para iniciar nossa demonstração, aproveitaremos `AI_QUERY()` para gerar avaliações falsas para usar em nosso pipeline de dados.

Os dados de amostra imitam avaliações de clientes sobre produtos de mercearia enviados a um site de comércio eletrônico, e criaremos um prompt para que a Open AI gere esses dados para nós.

Abra [03-Gerando-dados-fake-com-as-funcoes-de-AI]($./02-Gerando-dados-fake-com-as-funcoes-de-AI) para começar com sua primeira função SQL AI!


#### 3/ Construindo nosso pipeline SQL com Open AI para extrair sentimentos de revisão

Agora estamos prontos para criar nosso pipeline de dados completo:

&nbsp;
<img src="https://github.com/anasanchezss9/databricks_sql_e_openai/blob/main/images/sql-ai-function-flow.png?raw=true" width="1000">

Abra [04-automatizando-as-avaliacoes-e-respostas]($./03-automatizando-as-avaliacoes-e-respostas) para processar nosso texto usando SQL e automzatize o processo de análise de avaliações e criação de respostas personalizadas.

### Referência

Essa demonstração foi baseada na demonstração [SQL AI Functions](https://www.dbdemos.ai/demo.html?demoName=sql-ai-functions) do site  de tutoriais oficiais da Databricks.

### Leituras adicionais e recursos
- [Documentação](https://learn.microsoft.com/pt-br/azure/databricks/sql/language-manual/functions/AI_QUERY)
- [Apresentando funções de IA: Integrando modelos de linguagem grandes com Databricks SQL](https://www.databricks.com/blog/2023/04/18/introducing-ai-functions-integrating-large-language-models-databricks-sql.html)
- Confira mais demonstrações do Databricks no [Demo Center](https://www.databricks.com/resources/demos/tutorials?itm_data=demo_center)
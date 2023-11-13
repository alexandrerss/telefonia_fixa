# Passo a Passo da extração dos dados, manipulação, carregamento e demonstração dos dados.

# Objetivo
Este trabalho tem como objetivo a criação de um dashboard com as informações dos números de acessos do serviço de telefonia fixa no Brasil.
Todas as bases de dados deste trabalho foram extraídas do site da Anatel (Agência Nacional de Telecomunicações) no link https://informacoes.anatel.gov.br/paineis/acessos.

# Desafio - Tamanho dos dados
O primeiro desafio encontrado foi encontrar uma forma para o armazenamento dos dados devido ao seu tamanho. Os arquivos extraídos foram “acessos_historico.zip” e “acessos_banda_larga_fixa.zip” e estes dois arquivos possuem um total de 110 Mb com 22 arquivos e um total de 677 Mb extraídos.
Analisando as planilhas foi verificado que a planilha “Historico_Acessos.csv” seria a melhor base de dados para os valores totais anuais de acessos pois ela já retorna estes dados totais por ano.
Para realizar outras analises mais aprofundadas acerca do comportamento de suas características foi escolhida os csv sem o termo “Colunas” do título devido a distribuição dos dados. Mesmo com esta decisão o problema do tamanho total de dados permanece, agora com 5 arquivos e um total de 646 Mb extraídos.

# Solução Aplicada - SQL
Para este projeto, a maioria das planilhas estão com seus valores de quantidade de acessos informados por mês, como o propósito deste trabalho será de analisar a evolução por ano, vamos considerar apenas os valores do mês de dezembro para cada ano.
Para reduzirmos o tamanho das bases de dados e contar apenas com os dados que será de interesse para a análise foi utilizado alguns comandos em SQL.
A ferramenta utilizada foi a Dbeaver na versão 23.1.0.202306041918
Foi criado um banco de dados chamado “db_telefonia_fixa” e nele importado todos os 5 arquivos csv já separados.

# Manipulação dos dados em SQL
Para a planilha “Historico_Acessos.csv” não foi necessário realizar nenhuma manipulação. 
Na planilha “Acessos_Telefonia_Fixa_Total.CSV” foi executado um comando select para considerar apenas os dados do mês de dezembro de cada ano.

SELECT * 
FROM Acessos_Total 
WHERE Mês == 12

As planilhas de Autorizadas e Concessionárias possuem todas as colunas em comum. Foi analisado todas as colunas e verificado que algumas não seriam uteis em análise e assim foram descartadas para reduzir assim o tamanho das bases de dados a serem carregadas.
Foram descartadas as seguintes colunas: “CNPJ”, ”Código IBGE Municípios” e “Municípios”. Por fim aplicado também o filtro dos dados na coluna “Mês” considerando apenas o mês de dezembro de cada ano.

ALTER TABLE Autorizadas 
DROP COLUMN "Município";
ALTER TABLE Autorizadas
DROP COLUMN "Código IBGE Município";
ALTER TABLE Autorizadas
DROP COLUMN "Porte da Prestadora";
ALTER TABLE Autorizadas
DROP COLUMN "Tipo de Pessoa";

SELECT * 
FROM Autorizadas
WHERE Mês == 12

Para a planilha de Concessionarias além dos comandos acima foi realizado mais um comando, a exclusão da coluna de “Tipo do Acesso”
ALTER TABLE Concessionarias
DROP COLUMN "Tipo do Acesso";

Para a planilha de “Acessos_Telefonia_Fixa_Total” foi realizado os comandos abaixo, descarte das colunas de “Código IBGE”

ALTER TABLE Densidade 
DROP COLUMN "Código IBGE";

SELECT * 
FROM Densidade
WHERE Mês == 12

Em todos os casos foi utilizado o encoding ISO-8859-1 e não o UTF-8 devido aos acentos.

Para estes arquivos aplicados essa tratativa de dados usando comandos em SQL, o seu tamanho original de 677Mb e agora foi reduzido para apenas 30,6 Mb.

# Limpeza do Dataframes

Com a elaboração dos datasets a serem utilizados no código, agora a segunda parte é os comandos utilizados para a limpeza dos dataframes. Todas estas atividades abaixo não foram realizadas no SQL e sim diretamente no código Python “telefonia_fixa.py”
A base de histórico de acessos a partir de 2005 nos valores na coluna “Data” estavam com a informação de “1-ano”, sendo assim necessário retirar esse “1-“ antes de cada registro.
Para ser possível a realização de análises dos dados de acesso por região do Brasil, foi criado uma coluna denominada “Região” correspondente a região do pais de cada estado.
Foram encontrados também alguns dados em branco na coluna de "Grupo Econômico" , porém como temos a informação de CNPJ foi possivel assim prencher o nome de acordo com o CNPJ informado na coluna CNPJ.

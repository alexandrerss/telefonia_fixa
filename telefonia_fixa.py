# ==============================================================================
# IMPORTAR BIBLIOTECAS
# ==============================================================================

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
import json
from urllib.request import urlopen
import numpy as np


from millify import millify as mil
from PIL import Image

st.set_page_config(page_title='Telefonia Fixa', page_icon="📞")

# ==============================================================================
# IMPORTAR DATASETS 
# ==============================================================================

df = pd.read_csv ("datasets/Historico_Acessos.csv", sep= ';')
acessos = pd.read_csv ("datasets/Acessos_Total.csv", sep= ';', encoding='ISO-8859-1')
dens = pd.read_csv ("datasets/Densidade.csv", sep= ';', encoding='ISO-8859-1')
cons = pd.read_csv ("datasets/Concessionarias.csv", sep=';', encoding='ISO-8859-1',low_memory=False)
aut = pd.read_csv ("datasets/Autorizadas.csv", sep=';', encoding='ISO-8859-1')

# ==============================================================================
# LIMPEZA DOS DADOS
# ==============================================================================

# Limpeza de dados - Apagar os meses pra ficar apenas os valores de ano
df['Data'] = df['Data'].str.replace('01-', '')

# Conversao de texto/categoria/string para numeros inteiros
df['Data'] = df['Data'].astype( int )

dens['Densidade'] = dens['Densidade'].str.replace(',', '.').astype(float)

# União dos dataframes de autorizadas e concessões
telfixa = pd.concat([cons, aut])

#Inserir a Coluna de Região no dataframe
regioes = {
    'SP': 'Sudeste',
    'RJ': 'Sudeste',
    'MG': 'Sudeste',
    'ES': 'Sudeste',
    'PR': 'Sul',
    'SC': 'Sul',
    'RS': 'Sul',
    'DF': 'Centro Oeste',
    'GO': 'Centro Oeste',
    'MS': 'Centro Oeste',
    'MT': 'Centro Oeste',
    'BA': 'Nordeste',
    'SE': 'Nordeste',
    'AL': 'Nordeste',
    'PE': 'Nordeste',
    'PB': 'Nordeste',
    'RN': 'Nordeste',
    'CE': 'Nordeste',
    'MA': 'Nordeste',
    'PI': 'Nordeste',
    'TO': 'Norte',
    'PA': 'Norte',
    'AM': 'Norte',
    'AC': 'Norte',
    'RR': 'Norte',
    'RO': 'Norte',
    'AM': 'Norte',
    'AP': 'Norte',
}

# Adicionando a coluna 'Região' com base no mapeamento
telfixa['Região'] = telfixa['UF'].map(regioes)

# Aplicar a condição usando numpy.where() e preencher os valores em branco na coluna "Grupo Economico"
condicao_gvt = (telfixa['CNPJ'] == 3420926000124)
condicao_ebt = (telfixa['CNPJ'] == 33530486000129)
telfixa['Grupo Econômico'] = np.where(condicao_gvt, 'GVT', np.where(condicao_ebt, 'TELECOM AMERICAS', telfixa['Grupo Econômico']))

# ==============================================================================
# FUNÇÃO DOS FILTROS 
# ==============================================================================

def filtrar_por_intervalo_de_anos(df):
    data_limite = st.slider('Intervalo de anos desejado', 
                            value=(1972, 2022), 
                            min_value=1972, 
                            max_value=2022)
    
    # Filtro dos anos
    linhas_selecionadas = (df['Data'] >= data_limite[0]) & (df['Data'] <= data_limite[1])
    df = df.loc[linhas_selecionadas, :]
    return df

def aplicar_filtro_maroto(telfixa, coluna):
    reg = st.multiselect(f'Considerar quais categorias desejadas para análise na coluna {coluna}', 
                         telfixa[coluna].unique().tolist(),   
                         default=telfixa[coluna].unique().tolist())
    
    #if st.button("Aplicar Filtro"):
        # Aplicando o filtro de regiões
    linhas_selec = telfixa[coluna].isin(reg)
    telfixa = telfixa.loc[linhas_selec, :]
    
    return telfixa

# ==============================================================================
# BARRA LATERAL - SIDEBAR
# ==============================================================================

image_path = 'telefone.png'

image = Image.open (image_path)
st.sidebar.image(image, width=200)

st.sidebar.markdown(' # Telefonia Fixa no Brasil ')
st.sidebar.markdown(' ### Quantidade de acessos de Telefonia Fixa em todo o território nacional ')
st.sidebar.markdown("""---""")

st.sidebar.markdown('### Powered by Alexadrerss© 🌎🎓📊') 
with st.sidebar:
    components.html("""
                    <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="large" data-theme="light" data-type="VERTICAL" data-vanity="alexandrerss" data-version="v1"><a class="badge-base__link LI-simple-link" href=https://www.linkedin.com/in/alexandrerss/"></a></div>
                    <script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>              
              """, height= 310)
    
# ==============================================================================
# TELEFONIA FIXA
# ==============================================================================

st.title("📞 Telefonia Fixa")

st.markdown(
    """<div style="text-align: justify">
A telefonia fixa é transmitida por meio de um aparelho que fica ligado a outro telefone ou a uma central de condutores metálicos. O equipamento é composto por circuitos de conversação que se encarregam da voz e também por um circuito de marcação que é associado às chamadas telefônicas.</div>

Para este projeto foram utilizados os dados disponiveis no link : https://informacoes.anatel.gov.br/paineis/acessos</div>   

Data da última atualização em 27/09/2022.

""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['Total','Acessos por Ano','TUP', 'Concessão e Autorização','Regiões','Grupo Econômico','Tipo de Atendimento'])

with tab1:
    st.markdown('## Quantidade Totais no Brasil em 2022')

    col1, col2 =  st.columns(2)
    with col1:
        total_acesso = acessos[acessos['Ano'] == 2022]['Acessos'].sum()
        total_acesso_formatado = '{:,.2f}'.format(total_acesso)
        col1.metric('Total de Telefones Fixos no Brasil', total_acesso_formatado)
    with col2:
        total_dens = dens[(dens['Ano'] == 2022) & (dens['UF'] == 'Brasil')]['Densidade'].mean()
        total_dens_formatado = '{:,.2f}'.format(total_dens)
        col2.metric('Média Densidade de telefones fixos no Brasil', total_dens_formatado)


with tab2:
    df = filtrar_por_intervalo_de_anos(df)

    st.markdown('## Quantidade de Acessos por Ano')
    
    assinantes = df[df['Serviço'] == 'Telefonia Fixa']
    assinantes = assinantes[(df['Data'] != '2023') & (df['Tipo do Acesso'] == 'Individual em Serviço')]
    fig = px.bar(assinantes, x='Data', y='Acessos')
    fig.update_traces(marker_color = 'blue', marker_line_color = 'black', marker_line_width = 1, opacity = 1)
    st.plotly_chart(fig,use_container_width=True)
    
    st.dataframe (assinantes)

with tab3:
    st.markdown('## Quantidade de TUP (Orelhões) por ano')
    
    assinantes = df[df['Serviço'] == 'Telefonia Fixa']
    orelhao = assinantes[(df['Data'] != '2023') & (df['Tipo do Acesso'] == 'TUP')]
    fig =px.bar(orelhao, x='Data', y='Acessos')
    fig.update_traces(marker_color = 'blue', marker_line_color = 'black', marker_line_width = 1, opacity = 1)
    st.plotly_chart(fig,use_container_width=True)
    
    st.dataframe (orelhao)
    
with tab4:
    st.markdown('## Concessão e Autorização')
    
    outorga = acessos.loc[:, ['Ano', 'Tipo de Outorga', 'Acessos']].groupby(['Ano', 'Tipo de Outorga']).sum().sort_values('Ano', ascending=False).reset_index()
    fig = px.bar(outorga, x='Ano', y='Acessos', color='Tipo de Outorga', barmode='group')
    st.plotly_chart(fig,use_container_width=True)
    
    st.dataframe (outorga)
    
with tab5:
    st.markdown('## Total de Acesso - Regiões do Brasil em 2022')
    
    telfixa = aplicar_filtro_maroto(telfixa, "Região")
    
    regioes = telfixa.loc[:,['Região','Acessos','Ano']].groupby(['Ano','Região']).sum().reset_index()
    regioes = regioes[regioes['Ano'] == 2022]
    fig = px.bar(regioes, x='Região', y='Acessos',text_auto = '.3s')
    fig.update_traces(marker_color = 'blue', marker_line_color = 'black', marker_line_width = 1, opacity = 1)
    st.plotly_chart(fig,use_container_width=True)

    st.markdown('## Percentual total - Regiões do Brasil em 2022')

    fig = px.pie(regioes, values='Acessos', names='Região')
    fig.update_traces(marker = dict(line = dict(color = 'black', width = 2)))
    st.plotly_chart(fig,use_container_width=True)  
    
    st.markdown('## Curva de Evolução - Regiões do Brasil')
          
    regioes = telfixa.loc[:,['Região','Acessos','Ano']].groupby(['Ano','Região']).sum().reset_index()
    fig = px.line(regioes, x='Ano', y='Acessos', color='Região')
    st.plotly_chart(fig,use_container_width=True)
    
    st.markdown('## Total de Acessos - Estados do Brasil em 2022')
    
    estados = telfixa.loc[:,['Região','Acessos','Ano', 'UF']].groupby(['Ano','Região','UF']).sum().reset_index()
    estados = estados[estados['Ano'] == 2022]
    fig = px.scatter(estados, x='Região', y='UF', size='Acessos' ,color='Região',size_max = 20)
    st.plotly_chart(fig,use_container_width=True)

    # Geojson
    url = 'https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/brazil-states.geojson'

    with urlopen(url) as response:
        ccaa = json.load(response)

    fig = px.choropleth_mapbox(
        data_frame = estados,            # Data frame with values
        geojson = ccaa,                      # Geojson with geometries
        featureidkey = 'properties.sigla', # Geojson key which relates the file with the data from the data frame
        locations = 'UF',               # Name of the column of the data frame that matches featureidkey
        color = 'Acessos',                # Name of the column of the data frame with the data to be represented
        mapbox_style = 'open-street-map',
        center = dict(lat = -15.0, lon = -48),
        zoom = 2)

    st.plotly_chart(fig,use_container_width=True)  
    
with tab6:
    st.markdown('## Total de Acessos - Grupo Econômico em 2022' )
    
    telfixa = aplicar_filtro_maroto(telfixa,"Grupo Econômico")
       
    grupos = telfixa.loc[:,['Grupo Econômico','Acessos','Ano']].groupby(['Ano','Grupo Econômico',]).sum().reset_index()
    grupos = grupos[grupos['Ano'] == 2022]
    fig = px.bar(grupos, x='Grupo Econômico', y='Acessos',text_auto = '.3s')
    fig.update_traces(marker_color = 'blue', marker_line_color = 'black', marker_line_width = 1, opacity = 1)
    st.plotly_chart(fig,use_container_width=True)
    
    st.markdown('## Curva de Evolução - Grupo Econômico')
    
    
   
    grupos = telfixa.loc[:,['Grupo Econômico','Acessos','Ano']].groupby(['Ano','Grupo Econômico',]).sum().reset_index()
    fig = px.line(grupos, x='Ano', y='Acessos', color='Grupo Econômico')
    st.plotly_chart(fig,use_container_width=True)
    
with tab7:
    st.markdown('## Percentual de Tipo de Atendimento em 2022')  
      
    atend = telfixa.loc[:,['Tipo de Atendimento','Acessos','Ano']].groupby(['Ano','Tipo de Atendimento',]).sum().reset_index()
    atend = atend[atend['Ano'] == 2022]
    fig = px.pie(atend, names ='Tipo de Atendimento', values='Acessos',hole = 0.4)
    fig.update_traces(marker = dict(line = dict(color = 'black', width = 2)))
    st.plotly_chart(fig,use_container_width=True)

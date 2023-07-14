# Libraries
from PIL import Image
from datetime import datetime

from functions.funcEmpresa import *
from functions.funcEntregadores import *

st.set_page_config(page_title='Visão Entregadores',layout='wide')


#-----------------------------
# Inicio da estrutura lógica do código
#-----------------------------
# Import Dataset
df = pd.read_csv('train.csv')

# Limpeza dos dados
df1 = df.copy()

df1 = clean_code(df)

#Visão - Empresa
cols= ['ID','Order_Date']

#seleção de linhas
### Quantidade de pedidos por dia.
df_aux = df1.loc[:, cols].groupby( 'Order_Date' ).count().reset_index()
#=====================================
    # Layout Streamlit - Sidebar
#=====================================

st.header('Marketplace - Visão Entregadores')
image_path = 'logo.png'
image = Image.open (image_path)
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('# Fastest Delivery in Town')
st.sidebar.markdown("""___""")
st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider('Até qual valor?',
                  value=datetime(2022,4,13),
                  min_value=datetime(2022,2,11),
                  max_value=datetime(2022,4,6),
                  format='DD-MM-YYYY')

st.sidebar.markdown("""___""")


traffic_options= st.sidebar.multiselect('Quais as condições do trânsito',
                      ['Low','Medium','High','Jam'],
                      default='Low')
st.sidebar.markdown("""___""")
st.sidebar.markdown('###Powered by Wellington')

#filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas,:]

#filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas,:]

st.dataframe(df1)
#=====================================
    # Layout Streamlit - Tabs
#=====================================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial','',''])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns(4,gap='large')
        with col1:
            #A maior idade dos entregadores
            maior_idade = df1.loc[:,'Delivery_person_Age'].max()
            col1.metric('Maior de Idade', maior_idade)
            
        with col2:
            #A menor idade dos entregadores
            menor_idade = df1.loc[:,'Delivery_person_Age'].min()
            col2.metric('Menor Idade', menor_idade)
            
        with col3:
            #A maior idade dos entregadores
            melhor_condicao = df1.loc[:,'Vehicle_condition'].max()
            col3.metric('Melhor Condição', melhor_condicao)
            
        with col4:
            #A menor idade dos entregadores
            pior_condicao =df1.loc[:,'Vehicle_condition'].min()
            col4.metric('Pior Condição', pior_condicao)
            
    with st.container():
        st.markdown("""___""")
        st.title('Avaliacoes')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown ('##### Avaliação média por entregador')
            df_avg_ratings_per_delivery = df1.loc [:, ['Delivery_person_ID','Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(df_avg_ratings_per_delivery)
        with col2:
            st.markdown ('##### Avaliação média por trânsito')
            df_avg_rating_by_traffic = df1.loc [:, ['Delivery_person_Ratings','Road_traffic_density']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings':['mean', 'std']})
            #mudança nome das colunas
            df_avg_rating_by_traffic.columns = ['delivery_mean','delivery_std']
            #reset do index
            df_avg_rating_by_traffic.reset_index()
            st.dataframe(df_avg_rating_by_traffic)
            
            st.markdown ('##### Avaliação média por clima')
            df_avg_rating_by_weather = df1.loc [:, ['Delivery_person_Ratings','Weatherconditions']].groupby('Weatherconditions').agg({'Delivery_person_Ratings':['mean', 'std']})
            #mudança nome das colunas
            df_avg_rating_by_weather.columns = ['delivery_mean','delivery_std']
            #reset do index
            df_avg_rating_by_weather.reset_index()
            st.dataframe(df_avg_rating_by_weather)
            
    with st.container():
        st.markdown("""___""")
        st.title('Velocidade de Entrega')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown ('##### Top Entregadores mais rápidos')
            df3 = top_delivers(df1,top_asc=True)
            st.dataframe(df3)

            
        with col2:
            st.markdown ('##### Top Entregadores mais lentos')
            df3 = top_delivers(df1,top_asc=False)
            st.dataframe(df3)
            
          
               
        
    
    
    
    
    

# Libraries
import streamlit as st
from PIL import Image
from datetime import datetime

from functions.funcEmpresa import *

st.set_page_config(page_title='Visão Empresa',layout='wide')

#-----------------------------
# Inicio da estrutura lógica do código
#-----------------------------
# Import Dataset
df = pd.read_csv('train.csv')
df1 = clean_code(df)

    
#Visão - Empresa
cols= ['ID','Order_Date']

#seleção de linhas
### Quantidade de pedidos por dia.
df_aux = df1.loc[:, cols].groupby( 'Order_Date' ).count().reset_index()

    
#=====================================
    # Layout Streamlit - Sidebar
#=====================================

#Por exemplo aqui, st.header deveria ser invocado lá nas functions, aqui deveria-se chamar uma das functions
st.header('Marketplace - Visão Cliente')
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
tab1, tab2, tab3 = st.tabs(['Visão Gerencial','Visão Tática','Visão Geográfica'])

with tab1:
    with st.container():
        #Order Metric
        fig = order_metric(df1)
        st.markdown('# Orders by Day')
        st.plotly_chart(fig,us_container_width=True)
        
           
    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            fig = traffic_order_share(df1)
            st.header("Traffic Order Share")
            st.plotly_chart(fig,use_container_width=True)
            
            
            
        with col2:
            st.header("Traffic Order City")
            fig = traffic_order_city(df1)
            st.plotly_chart(fig,use_container_width=True)
            
            
            
with tab2:
    with st.container():
        st.header("Order by Week")
        fig = order_by_week(df1)
        st.plotly_chart(fig,use_container_width=True)
        
        
    with st.container():
        st.header("Order Share by Week")
        fig = order_share_by_week(df1)
        st.plotly_chart(fig,use_container_width=True)
        
        
with tab3:
    st.header("Country Maps")
    country_maps(df1)
    

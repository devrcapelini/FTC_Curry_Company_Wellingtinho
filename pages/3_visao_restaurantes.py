from PIL import Image
from datetime import datetime


from functions.funcEmpresa import *
from functions.funcRestaurante import *

st.set_page_config(page_title='Visão Restaurantes',layout='wide')

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
        st.title("Overall Metrics")
        
        col1,col2,col3,col4,col5,col6 = st.columns(6)
        
        with col1:
            delivery_unique = len(df1.loc[:,'Delivery_person_ID'].unique())
            col1.metric('Entregadores únicos',delivery_unique)
            
        with col2:
            avg_distance = distance(df1, fig=False)
            col2.metric('A distância média das entregas',avg_distance)
            
                
            
        with col3:
            df_aux = average_std_time_delivery(df1,'Yes','avg_time')
            col3.metric('Tempo Médio',df_aux)
            
  
        with col4:
            df_aux = average_std_time_delivery(df1,'Yes','std_time')
            col4.metric('STD Entrega c/ Festival',df_aux)        
            
        with col5:
            df_aux = average_std_time_delivery(df1,'No','avg_time')
            col5.metric('Tempo Médio ',df_aux)
            
            
        with col6:
            df_aux = average_std_time_delivery(df1,'No','std_time')
            col6.metric('STD Entrega c/ Festival',df_aux)
            
            
    with st.container():
        st.markdown("""___""")
        st.title("Tempo médio de entrega por cidade")
        cols = ['City','Time_taken(min)']
        df_aux = df1.loc[:, cols].groupby('City').agg({'Time_taken(min)':['mean','std']})
        df_aux.columns = ['avg_time','std_time']
        df_aux = df_aux.reset_index()
            
        fig = go.Figure()
        fig.add_trace(go.Bar( name='Control',x=df_aux['City'],y=df_aux['avg_time'],error_y=dict(type='data', array=df_aux['std_time'])))
            
        fig.update_layout(barmode='group')
        st.plotly_chart(fig)
        

    with st.container():
        st.markdown("""___""")
        st.title("Distribuição do Tempo")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = distance (df1, fig=True)    
            st.plotly_chart(fig)  
                              
            
        with col2:
            fig = avg_std_time_on_traffic(df1)
            st.plotly_chart(fig)
     
    
    with st.container():
        st.markdown("""___""")
        st.title("Distribuição da Distancia")
        cols = ['City','Time_taken(min)','Type_of_order']
        df_aux = df1.loc[:, cols].groupby(['City','Type_of_order']).agg({'Time_taken(min)':['mean','std']})
        df_aux.columns = ['avg_time','std_time']
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux)
        
        
        
           
            
            
            
            
          

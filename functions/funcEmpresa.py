import folium
import plotly.express as px
from streamlit_folium import folium_static
#Este import está aqui e está no código de regras de negócio (1_visao_empresa.py), seria mais limpo usar somente aqui.
import streamlit as st

#-----------------------------
# Funções
#-----------------------------
#função Map
def country_maps (df1):
    df_aux = df1.loc[:,['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']].groupby(['City','Road_traffic_density']).median().reset_index()
    df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
    map = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],location_info['Delivery_location_longitude']],
                           popup=location_info[['City','Road_traffic_density']]).add_to(map)
        folium_static(map, width=1024,height=600)
        


#função order share by week
def order_share_by_week(df1):
    df_aux01 = df1.loc[:,['ID','week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02 = df1.loc[:,['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
    df_aux = pd.merge(df_aux01, df_aux02, how ='inner', on='week_of_year')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')
            
    return fig


#função Order By Week
def order_by_week(df1):
    # criar a coluna de semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df_aux = df1.loc[:,['ID','week_of_year']].groupby('week_of_year').count().reset_index()
    fig = px.line(df_aux, x='week_of_year', y='ID')
    return fig
            
#função traffic order city
def traffic_order_city(df1):
                df_aux =df1.loc[:,['ID','City','Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()
                df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
                df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]
                fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
                return fig


#funçao Traffic Order Share
def traffic_order_share(df1):
                df_aux = df1.loc[:,['ID','Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
                df_aux = df_aux.loc[df_aux['Road_traffic_density'] != "NaN", :]
                df_aux['entregas_perc'] = df_aux['ID'] /df_aux['ID'].sum()
                fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
                st.plotly_chart(fig,use_container_width=True)
                return fig

#função order metric
def order_metric(df1):
    cols= ['ID','Order_Date']
    #seleção de linhas
    df_aux = df1.loc[:, cols].groupby( 'Order_Date' ).count().reset_index()
    # gráfico
    fig = px.bar( df_aux, x='Order_Date', y='ID' )
    return fig

# Limpeza dos dados
def clean_code(df1):
    """Esta função tem a responsabilidade de limpar o dataframe
        Tipos de limpeza:
        1 . Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços das variaveis de texto
        4. formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)
        Input: Dataframe
        Output: Dataframe
    """
    
    ## 1. convertendo a coluna Age de texto para número
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()


    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)


    ##  2. convertendo a coluna Ratings de texto para numero Decimal (Float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    ## 3. convertendo a coluna  order_date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format= '%d-%m-%Y')

    ## 4. convertendo multiple_deliverie de texto para numero inteiro(int)
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deiveries'] = df1 ['multiple_deliveries'].astype(int)

    ## 5. Removendo os espacos dentro de strings/texto/object
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    ##  7. Limpando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    return df1
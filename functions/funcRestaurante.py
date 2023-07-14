import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from haversine import haversine

#-----------------------------
# Funções
#-----------------------------
#função
def avg_std_time_on_traffic(df1):
    cols = ['City','Time_taken(min)','Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)':['mean','std']})
    df_aux.columns = ['avg_time','std_time']
    df_aux = df_aux.reset_index()

    fig = px.sunburst(df_aux, path=['City','Road_traffic_density'], values='avg_time',
                                  color='std_time', color_continuous_scale='RdBu',
                                  color_continuous_midpoint=np.average(df_aux['std_time']))

    return fig

#função grafico
def avg_std_time_graph(df1):
    cols = ['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
    df1['distance'] = df1.loc[:,cols].apply(lambda x: haversine(
                                           (x['Restaurant_latitude'],x['Restaurant_longitude']),
                                           (x['Delivery_location_latitude'],x['Delivery_location_longitude'])),axis=1)

    avg_distance = df1.loc[:,['City','distance']].groupby( 'City').mean().reset_index()
    fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'],pull=[0,0.1,0])])

    return fig

#Função average std time delivery
def average_std_time_delivery(df1,festival, op):
    """
        Esta função Calcula o tempo médio e o desvio padrão do tempo de entrega.
        parâmetros:
            input:
                - df: Dataframe com os dados necessários para o cálculo
                - op: Tipo de operação que precisa ser calculado
                        'avg_time': Calcula o tempo médio
                        'std_time': Calcula o desvio padrão do tempo
            Output:
                - df: Dataframe com 2 colunas e 1 linha.

    """
    df_aux = (df1.loc[:, ['Time_taken(min)','Festival']].groupby('Festival').agg({'Time_taken(min)':['mean','std']})) 
    df_aux.columns = ['avg_time','std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op],2)
    return df_aux

# Função distance
def distance(df1, fig):
    if fig == False:
        cols = ['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
        df1['distance'] = df1.loc[:,cols].apply(lambda x:haversine(
                                               (x['Restaurant_latitude'],x['Restaurant_longitude']),
                                               (x['Delivery_location_latitude'],x['Delivery_location_longitude'])),axis=1)
        avg_distance = np.round(df1['distance'].mean(), 2)
        return avg_distance
    else:
        cols = ['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']
        df1['distance'] = df1.loc[:,cols].apply(lambda x:haversine(
                                               (x['Restaurant_latitude'],x['Restaurant_longitude']),
                                               (x['Delivery_location_latitude'],x['Delivery_location_longitude'])),axis=1)
        avg_distance = np.round(df1['distance'].mean(), 2)
        avg_distance = df1.loc[:,['City','distance']].groupby( 'City').mean().reset_index()
        fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'],pull=[0,0.1,0])])
        return fig
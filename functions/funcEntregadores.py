import pandas as pd

#-----------------------------
# Funções
#-----------------------------
#função top_delivers
def top_delivers(df1,top_asc):
    df2 = df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']].groupby(['City','Delivery_person_ID']).max().sort_values(['City','Time_taken(min)'],ascending = top_asc).reset_index()
    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
    return df3
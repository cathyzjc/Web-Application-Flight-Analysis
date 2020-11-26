from distance import distance_df_final
import main
from controls import city_df, airport_df, routes_df, airlines_df

start_city = 'Boston'
start_airport = 'JFK'
end_airport = 'LGA'

df = distance_df_final
df_choose = airport_df[airport_df.IATA == start_airport].iloc[0]['Tz database time zone']

print(df_choose)

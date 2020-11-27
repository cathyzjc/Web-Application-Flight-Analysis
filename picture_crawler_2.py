from distance import distance_df_final
import main
from controls import city_df, airport_df, routes_df, airlines_df
import picture_crawler

i = 0
all = len(list(city_df.City))
for city in list(city_df.City):
    picture_crawler.download(city)
    i += 1
    print('Progress:', i, "/", all, "Percentage", i/all*100, "%")

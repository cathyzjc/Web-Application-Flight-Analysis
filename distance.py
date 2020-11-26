from controls import city_df, airport_df, routes_df, airlines_df
import pandas as pd
import math

def compute_distance_in_kilometers(lon1, lat1, lon2, lat2):
    phi_1 = lat1 * math.pi / 180.0
    phi_2 = lat2 * math.pi / 180.0
    change_phi = (lat2 - lat1) * math.pi / 180
    change_lambda = (lon2 - lon1) * math.pi / 180

    a = math.sin(change_phi / 2.0) * math.sin(change_phi / 2.0) + \
        math.cos(phi_1) * math.cos(phi_2) * math.sin(change_lambda / 2.0) * math.sin(change_lambda / 2.0)
    c = 2.0 * math.atan2(math.sqrt(a),math.sqrt(1.0 - a))
    return 6371.0 * c


pd.set_option('display.max_columns', None)
start_df = airport_df.set_index('IATA')
end_df = airport_df.set_index('IATA')

distance_df_1 = routes_df.set_index('Source airport')
distance_df_2 = distance_df_1.join(start_df, lsuffix='_route', rsuffix='_start')
distance_df_2['Start_airport'] = distance_df_2.index
distance_df_3 = distance_df_2.set_index('Destination airport')
distance_df_4 = distance_df_3.join(end_df, lsuffix='_start', rsuffix='_end')
distance_df_4['End_airport'] = distance_df_4.index
distance_df_5 = distance_df_4.reset_index(drop=True)


distance_df_6 = pd.DataFrame(distance_df_5, columns = ["Start_airport",'End_airport',
                                                           'Name_start','Name_end',
                                                           'City_start','City_end',
                                                           'Latitude_start','Latitude_end',
                                                           'Longitude_start','Longitude_end',
                                                           'Altitude_start','Altitude_end'])
distance_df_7= distance_df_6.drop_duplicates()


def calculate_distance(x):
    return compute_distance_in_kilometers(x.Longitude_start, x.Latitude_start, x.Longitude_end,x.Latitude_end)


distance_df_final = distance_df_7.copy()
distance_df_final["Distance"] = distance_df_7.apply(calculate_distance, axis = 1)

# print(distance_df_final)
# Web-Application-Flight-Analysis
 
The web application Kartemap is built using the Python Dash framework. You can easily check the most convenient flight between the departure airport and the arrival airport. 
    
        
            
            

## 1. Data Contained:

1. city data - contained most cities who own airport in US
2. city image - each city owns a unique image
3. flight route data - direct flight between each airports and their distancec (calculated from airport long\lat coordinates)
4. airport data - all airports located in US, also contain information about timezone, location, city etc.
5. airline data - all airline in US
    
        
        

## 2. Algorithm

1. Model analytics to compute distances from city long\lat coordinates.
2. Network Analysis (main.py) to compute the least cost path between a start and end node.
3. If there exists direct flight between two airports, prefer direct flight rather than Network Analysis.
    
        
        
## 3. Python Files

> ### 3.1 app.py

> The web application file built on Python Dash Framework.    
    
    

> ### 3.2 picture_crawler.py & picture_crawler_2.py

> Web crawler functions. Source: [Baidu Image](https://image.baidu.com/)     


> ### 3.3 distance.py

> Generate dataframe **distance_df_final**, which contains start airport, end airport and their distance.
Distance is calculated by Haversine Formula.    


> ### 3.4 main.py

> **Network Analysis** to compute **the nearest path** between the start airport and the end airport **if there is no direct flight**.     

    
        
        


## 4 Website Layout

1. Search bar to choose the city and airport you want to check
2. Flight map which shows how the flight is 
3. Conclusion of how your flight should perform and how many stops
4. More informations about departure and arrival flight, and COVID-19 related information
5. Pictures of departure city and arrival city

# Web-Application-Flight-Analysis
 
The web application Kartemap is built using the Python Dash framework. You can easily check the most convenient flight between the departure airport and the arrival airport. 


## Data Contained:

city data - contained all cities who own airport in US
flight route data - direct flight between each airports and their distancec (calculated from airport long\lat coordinates)
airport data - all airports located in US, also contain information about timezone, location, city etc.
airline data - all airline in US


## Algorithm

1. Model analytics to compute distances from city long\lat coordinates.
2. Network Analysis (main.py) to compute the least cost path between a start and end node.
3. If there exists direct flight between two airports, prefer direct flight rather than Network Analysis.

## Website Layout

1. Search bar to choose the city and airport you want to check
2. Flight map which shows how the flight is 
3. Conclusion of how your flight should perform and how many stops
4. More informations about departure and arrival flight, and COVID-19 related information

from algorithms.shortest_path import Dijkstra
from graph.network import Network
from distance import distance_df_final

def read_network_from_file(df):
    """ Read from a file and build a network
    file_name: file to read from
    delimeter: delimeter that separates fields
    """
    airports = list()
    distances = dict()

    for row in df.itertuples():
        airport_1 = row.Start_airport
        airport_2 = row.End_airport
        distance = round(row.Distance)

        # build the list of cities
        if airport_1 not in airports:
            airports.append(airport_1)
        if airport_2 not in airports:
            airports.append(airport_2)

        # build the dictionary based on city distances
        if airports.index(airport_1) not in distances.keys():
            distances[airports.index(airport_1)] = {airports.index(airport_2): distance}
        if airports.index(airport_2) not in distances[airports.index(airport_1)].keys():
            distances[airports.index(airport_1)][airports.index(airport_2)] = distance

    return airports, distances


def main(start_airport, target_node):
    # application salutation
    application_name = 'Network Analysis'
    # print('-' * len(application_name))
    # print(application_name)
    # print('-' * len(application_name))

    try:
    # read network from file
        airports, distances = read_network_from_file(distance_df_final)

    # build the network
        network = Network()
        network.add_nodes(airports)
        for connection in distances.items():
            frm = airports[connection[0]]
            for connection_to in connection[1].items():
                network.add_edge(frm, airports[connection_to[0]], connection_to[1])

    # uncomment to print the network
    # print(network)

    # get from user the start city
    # for (index, city) in enumerate(network.get_nodes()):
        # print(f'{index}: {city:s}')

    # using Dijkstra's algorithm, compute least cost (distance)
    # from start city to all other cities
        Dijkstra.compute(network, network.get_node(start_airport))

    # show the shortest path(s) from start city to all other cities
    # print('\nShortest Paths')

        target_city = network.get_node(target_node)
        path = [target_city.get_name()]
        Dijkstra.compute_shortest_path(target_city, path)
    except AttributeError:
        return [None, None, None, None]
    else:
        return [start_airport, target_node, path[::-1], target_city.get_weight()]

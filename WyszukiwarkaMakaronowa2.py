import csv


def find_shortest_path(start, end, max_intermediates=4):
    with open('Zeszyt1.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        connections = {}
        for row in reader:
            start_city = row['Rozpoczecie']
            end_city = row['Zakonczenie']
            distance = int(row['km'])
            if start_city not in connections:
                connections[start_city] = {}
            connections[start_city][end_city] = distance

        intermediates = []
        shortest_distance = float('inf')
        shortest_path = []
        for intermediate_count in range(max_intermediates + 1):
            for intermediate in intermediates:
                for start_city, distance in connections[intermediate].items():
                    if start_city == end:
                        path = [intermediate, start_city]
                        if intermediate_count == 0:
                            path = [start]
                        path_distance = distance
                        if path_distance < shortest_distance:
                            shortest_distance = path_distance
                            shortest_path = path
                    elif start_city not in intermediates:
                        path = [intermediate, start_city, end]
                        if intermediate_count == 0:
                            path = [start, start_city, end]
                        path_distance = distance + connections[start_city][end_city]
                        if path_distance < shortest_distance:
                            shortest_distance = path_distance
                            shortest_path = path
            intermediates += connections.keys()

        return shortest_path, shortest_distance
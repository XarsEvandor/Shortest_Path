import networkx as nx

G = nx.DiGraph()
G.add_node(1, name="Earth", visited=False)
G.add_node(2, name="Jupiter", visited=False)
G.add_node(3, name="Saturn", visited=False)
G.add_node(4, name="Ceres", visited=False)
G.add_edge(1, 2, weight=637092)
G.add_edge(1, 3, weight=1287054)
G.add_edge(1, 4, weight=264400)
G.add_edge(2, 3, weight=658054)
G.add_edge(2, 4, weight=364600)
G.add_edge(3, 2, weight=662992)
G.add_edge(3, 4, weight=1019500)
G.add_edge(4, 2, weight=372692)
G.add_edge(4, 3, weight=1022654)

planet_name = nx.get_node_attributes(G, 'name')
planet_visited = nx.get_node_attributes(G, 'visited')

node_num = nx.number_of_nodes(G)


# print(node_num)

def bruteForce():
    minN = 0
    minK = 0
    minL = 0
    king = 0

    # Brute force method.
    for n in range(2, node_num + 1):
        for k in range(1, node_num + 1):
            if n == k:
                continue
            if k == 1:
                continue
            for l in range(1, node_num + 1):
                if n == k or n == l or k == l:
                    continue
                if l == 1:
                    continue
                try:
                    total_weight = G[1][n]["weight"] + G[n][k]["weight"] + G[k][l]["weight"]
                except:
                    continue

                if total_weight < king:
                    king = total_weight
                    minN = n
                    minK = k
                    minL = l
                # Combination Unique to the first iteration.
                elif n == 2 and k == 3 and l == 4:
                    king = total_weight
                    minN = n
                    minK = k
                    minL = l
                print(planet_name[1] + " -> " + planet_name[n]
                      + " -> " + planet_name[k] + " -> " + planet_name[l] + "     Weight: " + str(total_weight))

    print("The optimal path is " + planet_name[1] + " -> " + planet_name[minN]
          + " -> " + planet_name[minK] + " -> " + planet_name[minL])

    txt = "With a total distance of: {king:,} km"
    print(txt.format(king=king))


# Nearest neighbor method

def shortestNeighbor():
    # We always start from earth
    nextStop = 1
    kinglist = []
    weight_sum = 0

    print("\n\nThe optimal path is: ")

    for n in range(1, node_num):
        neighborlist = []
        iterHolder = iter(G.neighbors(nextStop))
        # Populate neighbor list with the iterated neigbors of the nextStop node
        while True:
            try:
                neighborlist.append(next(iterHolder))
            except StopIteration:
                break

            # Set the king as the first non visited planet out of the neighbors of nextStop
            king = next(
                filter(lambda planet: not planet_visited[planet], neighborlist), None)
        for k in neighborlist:
            # Avoid same planet travel
            if nextStop == k or nextStop == king:
                continue
            # Avoid visited planets
            if planet_visited[k]:
                continue
            # Checks for the shortest path
            if G[nextStop][king]["weight"] > G[nextStop][k]["weight"]:
                king = k

        print(planet_name[nextStop] + " -> " + planet_name[king])
        weight_sum += G[nextStop][king]["weight"]
        # Mark the planet as visited
        planet_visited[nextStop] = True
        # The next stop is the shortest neighbor of the previous nextStop
        nextStop = king

    txt = "with a total distance of: {weight_sum:,} km"
    print(txt.format(weight_sum=weight_sum))


bruteForce()
shortestNeighbor()

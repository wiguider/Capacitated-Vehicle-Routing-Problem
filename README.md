# A solution approach to the capacitated vehicle routing problem


The VRP is concerned with the determination of the optimal routes used by a fleet of vehicles, based at one or more depots, to serve a set of customers. Many additional requirements and operational constraints are imposed on the route construction in practical applications of the VRP. For example, the service may
involve both deliveries and collections, the load along each route must not exceed the given capacity of the vehicles, the total length of each route must not be greater than a prescribed limit, the service of the customers must occur within given time windows, the fleet may contain heterogeneous vehicles, precedence relations may exist between the customers, the customer demands may not be completely known in advance,
the service of a customer may be split among different vehicles, and some problem characteristics, as the demands or the travel times, may vary dynamically.

We consider the static and deterministic basic version of the problem, known as the capacitated VRP
(CVRP).
In the CVRP all the customers correspond to deliveries, the demands are deterministic, known in advance
and may not be split, the vehicles are identical and are based at a single central depot, only the capacity restrictions for the vehicles are imposed, and the objective is to minimize the total cost (i.e., the number of routes and/or their length or travel time) needed to serve all the customers. Generally, the travel cost between each pair of customer locations is the same in both directions, i.e., the resulting cost matrix is symmetric, whereas in some applications, as the distribution in urban areas with one-way directions imposed on the roads, the cost matrix is asymmetric.
The CVRP has been extensively studied since the early sixties and in the last years, many new heuristic and exact approaches were presented. The largest problems which can be consistently solved by the most effective exact algorithms proposed so far contain about 50 customers, whereas larger instances may be solved only in particular cases. So instances with hundreds of customers, as those arising in practical applications, may only be tackled with heuristic methods.

The CVRP extends the well-known Traveling Salesman Problem (TSP), calling for the determination of the circuit with associated minimum cost, visiting exactly once a given set of points. Therefore, many exact approaches for the CVRP were inherited from the huge and successful work done for the exact solution of the TSP.

##How to run the project:

To get the project up and running please execute the following command:

    '/bin/sh /Path/to/the/project/cvrpb/job.sh'

You can find the resulting files are generated under 'Results' directory and they will overwrite the old ones.

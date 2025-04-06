# Minimum Temporal Paths
Temporal graphs are special graphs that can change their configuration overtime. In particular, every edge of the graph can be traversed in a specific time instance and takes a certain amount of time to reach the following node. Due to additional temporal information, the concept of computing shortest paths in temporal graphs widely differs from the traditional static one. Articles have studied and analyzed a series of shortest paths, which minimize certain metrics in temporal graphs. These are collectively called minimum temporal paths.
- Earliest-arrival path, the path with minimum arrival time
- Latest-departure path, the path that maximazes its starting time while reaching a destination by a given time
- Fastest path, the path with minimum duration, meaning the total amount of time traveled from source to destination
- Shortest path, the with minimum distance, meaning the total traversing time of all the edges traversed

The article "Path Problems in Temporal Graphs" provides a series of algorithms to effciently compute these temporal paths. The folder algorithms contains the Python implementation of some of them.

To test these implementations, we need to generate at least one temporal graph and apply the algorithms. The file randomGraphs can generate random temporal graphs with the following characteristics:
- all edges' activation times are distinct
- all edges can be traversed in one time istance

The following static models have been used as a basis for generating temporal graphs:
- Erdős–Rényi
- Random Regular Graphs

import math
from typing import Dict, List, Tuple
import time


class Graph:
    def __init__(self):
        self.n = 0  # |V|
        self.m = 0  # |E|
        self.k = 0  # the exponent k
        self.s = 0  # source id
        self.t = 0  # target id
        # map vertex_id -> (x,y)
        self.vertices: Dict[int, Tuple[float, float]] = {}
        # list of undirected edges
        self.edges: List[Tuple[int, int]] = []

    @classmethod
    def read_graph_from_file(cls, filename: str) -> "Graph":
        """
        File format:
          first line:  n m k s t
          next n lines:  id x y
          next m lines:  u v
        """
        g = cls()
        with open(filename, "r") as f:
            line = f.readline().strip()
            g.n, g.m, g.k, g.s, g.t = map(int, line.split())

            for _ in range(g.n):
                vid, x, y = map(float, f.readline().split())
                g.vertices[int(vid)] = (x, y)

            for _ in range(g.m):
                u, v = map(int, f.readline().split())
                g.edges.append((u, v))
        return g

    def shortest_path(self) -> Tuple[float, List[int], int]:
        """
        Bellman–Ford on an undirected graph with weight D(u,v,k).
        Returns (distance, path, visited_count).
        - distance = dist[t] or math.inf if unreachable
        - path = sequence of vertex‐IDs from s to t (or [] if none)
        - visited_count = number of vertices with finite dist
        """
        # 1. shortcut to coords
        coords = self.vertices

        # 2. D(u,v,k) as specified
        def D(u: int, v: int) -> float:
            x1, y1 = coords[u]
            x2, y2 = coords[v]
            dx, dy = abs(x1 - x2), abs(y1 - y2)
            if self.k == 0:
                return 1.0
            if self.k < 0 or math.isinf(self.k):
                return float(max(dx, dy))
            return (dx**self.k + dy**self.k) ** (1.0 / self.k)

        # 3. init dist & predecessor
        dist: Dict[int, float] = {v: math.inf for v in coords}
        pred: Dict[int, int] = {v: None for v in coords}
        dist[self.s] = 0.0

        # 4. relax edges up to n-1 times
        for _ in range(self.n - 1):
            updated = False
            for u, v in self.edges:
                w = D(u, v)
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    pred[v] = u
                    updated = True
                if dist[v] + w < dist[u]:
                    dist[u] = dist[v] + w
                    pred[u] = v
                    updated = True
            if not updated:
                break

        # 5. negative‐cycle check (should never fire since k>=-1 & all weights>=0)
        for u, v in self.edges:
            w = D(u, v)
            if dist[u] + w < dist[v] or dist[v] + w < dist[u]:
                raise ValueError("Negative‐weight cycle detected")

        # 6. reconstruct path s→t
        path: List[int] = []
        if dist[self.t] < math.inf:
            cur = self.t
            while cur is not None:
                path.append(cur)
                cur = pred[cur]
            path.reverse()

        # 7. count reachable
        visited_count = sum(1 for d in dist.values() if d < math.inf)

        return dist[self.t], path, visited_count


def main():
    graph = Graph.read_graph_from_file("5000.txt")
    print(graph.n, graph.m, graph.k, graph.s, graph.t, "\n")

    start = time.perf_counter()
    distance, path, visited = graph.shortest_path()
    end = time.perf_counter()

    print(f"visited = {visited}")
    print(f"distance = {distance}")
    print(f"path = {path}")
    print(f"elapsed = {end - start:.6f} seconds")


if __name__ == "__main__":
    main()

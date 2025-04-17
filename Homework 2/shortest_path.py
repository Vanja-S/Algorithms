from collections import defaultdict
import math
import heapq
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
        A* search from self.s to self.t on the undirected graph.
        Uses D(u,v,k) as edge‐weight and h(u)=D(u,self.t,k) as heuristic.
        Returns (distance, path_list, visited_count).
        """
        # 1. coordinate lookup
        coords: Dict[int, Tuple[float, float]] = self.vertices

        # 2. weight D(u,v) as before
        def D(u: int, v: int) -> float:
            x1, y1 = coords[u]
            x2, y2 = coords[v]
            dx, dy = abs(x1 - x2), abs(y1 - y2)
            k = self.k
            if k == 0:
                return 1.0
            if k < 0 or math.isinf(k):
                return float(max(dx, dy))
            return (dx**k + dy**k) ** (1.0 / k)

        # 3. heuristic h(u) = D(u, t)
        def h(u: int) -> float:
            return D(u, self.t)

        # 4. build adjacency list (undirected)
        nbrs: Dict[int, List[int]] = defaultdict(list)
        for u, v in self.edges:
            nbrs[u].append(v)
            nbrs[v].append(u)

        # 5. A* structures
        g_score: Dict[int, float] = {v: math.inf for v in coords}
        f_score: Dict[int, float] = {v: math.inf for v in coords}
        came_from: Dict[int, int] = {}
        open_heap: List[Tuple[float, int]] = []

        # init
        g_score[self.s] = 0.0
        f_score[self.s] = h(self.s)
        heapq.heappush(open_heap, (f_score[self.s], self.s))

        closed: set[int] = set()
        visited_count = 0

        while open_heap:
            f_u, u = heapq.heappop(open_heap)
            if u in closed:
                continue

            closed.add(u)
            visited_count += 1

            # goal check
            if u == self.t:
                break

            # relax neighbors
            for v in nbrs[u]:
                if v in closed:
                    continue
                tentative_g = g_score[u] + D(u, v)
                if tentative_g < g_score[v]:
                    came_from[v] = u
                    g_score[v] = tentative_g
                    f_score[v] = tentative_g + h(v)
                    heapq.heappush(open_heap, (f_score[v], v))

        # reconstruct path
        path: List[int] = []
        if self.t in came_from or self.s == self.t:
            cur = self.t
            path.append(cur)
            while cur != self.s:
                cur = came_from[cur]
                path.append(cur)
            path.reverse()

        dist_t = g_score[self.t]
        if math.isinf(dist_t):
            path = []

        return dist_t, path, visited_count


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

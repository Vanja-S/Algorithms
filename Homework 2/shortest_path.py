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
        self.vertices: Dict[str, Tuple[float, float]] = {}
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

    def shortest_path(self) -> Tuple[float, List[str], int]:
        """
        A* from self.s to self.t.  Returns (distance, path, visited_count).
        - distance: g(self.t) or math.inf if no path
        - path: list of vertex-ids from s to t (empty if unreachable)
        - visited_count: number of distinct nodes popped from the open set
        """
        coords = self.vertices

        # 1. edge‐weight D(u,v,k)
        def D(u: str, v: str) -> float:
            x1, y1 = coords[u]
            x2, y2 = coords[v]
            dx, dy = abs(x1 - x2), abs(y1 - y2)
            k = self.k
            if k == 0:
                return 1.0
            if k < 0 or math.isinf(k):
                return float(max(dx, dy))
            return (dx**k + dy**k) ** (1.0 / k)

        # 2. heuristic h(u) = D(u, t)
        def h(u: str) -> float:
            return D(u, self.t)

        # 3. build undirected adjacency list
        nbrs: Dict[str, List[str]] = defaultdict(list)
        for u, v in self.edges:
            nbrs[u].append(v)
            nbrs[v].append(u)

        # 4. A* bookkeeping
        g_score: Dict[str, float] = {v: math.inf for v in coords}
        f_score: Dict[str, float] = {v: math.inf for v in coords}
        came_from: Dict[str, str] = {}

        open_heap: List[Tuple[float, str]] = []
        g_score[self.s] = 0.0
        f_score[self.s] = h(self.s)
        heapq.heappush(open_heap, (f_score[self.s], self.s))

        closed: set[str] = set()
        visited_count = 0

        # 5. main loop
        while open_heap:
            f_u, u = heapq.heappop(open_heap)
            if u in closed:
                continue

            closed.add(u)
            visited_count += 1

            if u == self.t:
                break

            for v in nbrs[u]:
                if v in closed:
                    continue
                tentative_g = g_score[u] + D(u, v)
                if tentative_g < g_score[v]:
                    came_from[v] = u
                    g_score[v] = tentative_g
                    f_score[v] = tentative_g + h(v)
                    heapq.heappush(open_heap, (f_score[v], v))

        # 6. reconstruct path
        path: List[str] = []
        if g_score[self.t] < math.inf:
            cur = self.t
            while cur != self.s:
                path.append(cur)
                cur = came_from[cur]
            path.append(self.s)
            path.reverse()
        else:
            # unreachable
            path = []

        return g_score[self.t], path, visited_count


def main():
    graph = Graph.read_graph_from_file("5000.txt")
    print(graph.n, graph.m, graph.k, graph.s, graph.t, "\n")

    distance, path, visited = graph.shortest_path()

    print(f"{visited}")
    print(f"{distance}")
    print(f"{path}")


if __name__ == "__main__":
    main()

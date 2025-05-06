from typing import Dict, List, Tuple
import os
import random


# We will use a grid graph for the instances


def gen_instance(n, m, k, s, t):
    """
    Generates a graph instance with specified parameters.

    Args:
      n (int): The number of vertices in the graph.
      m (int): The number of edges in the graph.
      k (int): A parameter for additional constraints or properties (usage depends on context).
      s (int): The source vertex identifier.
      t (int): The target vertex identifier.

    Returns:
      None: The function initializes and populates the `vertices` and `edges` data structures.
    """
    vertices: Dict[str, Tuple[float, float]] = {}
    edges: List[Tuple[int, int]] = []
    # Create the file path
    file_path = os.path.join(os.path.dirname(__file__), f"{n}.txt")
    print(file_path)

    # Generate vertices with random coordinates

    grid_size = int(n**0.5)
    for i in range(grid_size):
        for j in range(grid_size):
            x, y = i * (100 / (grid_size - 1)), j * (100 / (grid_size - 1))
            vertices[i * grid_size + j] = (x, y)

    # Generate edges for a square grid graph
    for i in range(int(n**0.5)):
        for j in range(int(n**0.5)):
            current = i * int(n**0.5) + j
            if j + 1 < int(n**0.5):  # Horizontal edge
                edges.append((current, current + 1))
            if i + 1 < int(n**0.5):  # Vertical edge
                edges.append((current, current + int(n**0.5)))

    # Write to the file
    with open(file_path, "w") as f:
        # Write the first line
        f.write(f"{n} {m} {k} {s} {t}\n")

        # Write the vertices
        for i, (x, y) in vertices.items():
            f.write(f"{i} {x:.2f} {y:.2f}\n")

        # Write the edges
        for idx, (u, v) in enumerate(edges):
            f.write(f"{u} {v}\n")


def num_of_edges_in_square_grid_graph(n):
    return 2 * n * n - 2 * n


def main():
    gen_instance(100, num_of_edges_in_square_grid_graph(100), -1, 0, 100)
    gen_instance(500, num_of_edges_in_square_grid_graph(500), 0, 0, 500)
    gen_instance(1000, num_of_edges_in_square_grid_graph(1000), 1, 0, 1000)
    gen_instance(5000, num_of_edges_in_square_grid_graph(5000), 2, 0, 5000)
    gen_instance(10000, num_of_edges_in_square_grid_graph(10000), 3, 0, 10000)


if __name__ == "__main__":
    main()

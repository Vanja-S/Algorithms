class BinaryTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class ZigZag:
    def __init__(self, root):
        self.tree = root

    def show(self):
        if not self.tree:
            return []

        current_level = []
        next_level = []
        current_level.append(self.tree)

        left_to_right = True
        result = []
        level = []

        while current_level:
            level_size = len(current_level)
            level = []

            for _ in range(level_size):
                node = current_level.pop()
                level.append(node.value)

                if left_to_right:
                    if node.left:
                        next_level.append(node.left)
                    if node.right:
                        next_level.append(node.right)
                else:
                    if node.right:
                        next_level.append(node.right)
                    if node.left:
                        next_level.append(node.left)

            result.extend(level)

            left_to_right = not left_to_right
            current_level, next_level = next_level, []

        print(" ".join(map(str, result)))

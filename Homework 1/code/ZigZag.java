import java.util.*;

class ZigZag {
    Node tree;

    public ZigZag(Node root) {
        tree = root;
    }

    public void show() {
        if (tree == null) {
            return;
        }

        Stack<Node> currentLevel = new Stack<>();
        Stack<Node> nextLevel = new Stack<>();
        currentLevel.push(tree);
        
        boolean leftToRight = true;
        StringBuilder result = new StringBuilder();

        while (!currentLevel.isEmpty()) {
            Node node = currentLevel.pop();
            result.append(node.value).append(" ");

            if (leftToRight) {
                if (node.left != null) {
                    nextLevel.push(node.left);
                }
                if (node.right != null) {
                    nextLevel.push(node.right);
                }
            } else {
                if (node.right != null) {
                    nextLevel.push(node.right);
                }
                if (node.left != null) {
                    nextLevel.push(node.left);
                }
            }

            if (currentLevel.isEmpty()) {
                leftToRight = !leftToRight;
                Stack<Node> temp = currentLevel;
                currentLevel = nextLevel;
                nextLevel = temp;
            }
        }

        System.out.println(result.toString().trim());
    }
}
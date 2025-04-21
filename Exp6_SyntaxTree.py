class Node:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def inorder(node):
    if node:
        if node.left: print("(", end="")
        inorder(node.left)
        print(node.val, end="")
        inorder(node.right)
        if node.right: print(")", end="")

tree = Node('*', Node('+', Node('a'), Node('b')), Node('c'))
inorder(tree)
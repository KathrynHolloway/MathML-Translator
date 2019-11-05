class Node:
    def __init__(self, name, child, sibling, attributes):
        self.name = name
        self.child = child
        self.sibling = sibling
        self.attributes = attributes

    def get_name(self):
        return self.name

    def get_child(self):
        return self.child

    def get_sibling(self):
        return self.sibling
    
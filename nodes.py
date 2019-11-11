from abc import ABC, abstractmethod #note that the later is a decorator
class Node(ABC):
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

    @abstractmethod
    def get_name(self):
        pass
        return self.name

    # @abstractmethod
    # def get_child(self):
    #     pass
    #     return self.child
    #
    # @abstractmethod
    # def get_sibling(self):
    #     pass
    #     return self.sibling
    '''add get attributes?'''

    @abstractmethod
    def outputxml(self):
        pass

class Value(Node):
    #values are numbers and leaves so by definition, no children
    def __init__(self, name, sibling, attributes):
        super().__init__(name, attributes)
        self.sibling = sibling

    def get_name(self):
        return self.name

    # def get_child(self):
    #     return self.child

    def get_sibling(self):
        return self.sibling

    def outputxml(self):
        pass
    
class Operator(Node):
    def __init__(self, name, child, sibling, attributes):
        super().__init__(name, attributes)
        self.child = child
        self.sibling = sibling

    def get_name(self):
        return self.name

    def get_child(self):
        return self.child

    def get_sibling(self):
        return self.sibling
    # operators can have siblings

    def outputxml(self):
        pass

class NoSibOperator(Node): # some operators eg sup won't have more than a child ?
    def __init__(self, name, child, attributes):
        super().__init__(name, attributes)
        self.child = child

    def get_name(self):
        return self.name

    def get_child(self):
        return self.child

    def outputxml(self):
        pass

class Identifier(Node):
    def __init__(self, name, sibling, attributes):
        super().__init__(name, attributes)
        self.sibling = sibling

    def get_name(self):
        return self.name
    
    # def get_child(self):
    #     return self.child
    #is a leaf so by definition cannot have a child

    def get_sibling(self):
        return self.sibling

    def outputxml(self):
        pass
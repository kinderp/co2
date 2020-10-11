from anytree import NodeMixin, RenderTree

class Block(NodeMixin):
    def __init__(self, name, parent=None, children=None):
        self.__name = name
        self.parent = parent
        if children:
            self.children = children

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def render(self):
        for pre, fill, node in RenderTree(self):
            print("{}{}".format(pre, node.name))

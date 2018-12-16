from __future__ import annotations
from functools import reduce
import string


class TreeNode:
    letters = list(string.ascii_uppercase)
    id = 0

    def __init__(self):
        self.id = TreeNode.id
        TreeNode.id += 1
        self.links = []
        self.metadata = []

    def add_link(self, link: TreeNode):
        self.links.append(link)

    def add_metadata(self, metadata):
        self.metadata.append(int(metadata))

    def metadata_sum(self) -> int:
        self_sum = sum(self.metadata)
        for node in self.links:
            self_sum += node.metadata_sum()
        return self_sum

    def value(self) -> int:
        if not self.links:
            return sum(self.metadata)
        res = 0
        for md in self.metadata:
            if len(self.links) >= md:
                res += self.links[md - 1].value()
        return res

    def __repr__(self):
        res = "Node #{}\n".format(self.id)
        res += "Links = {}\n".format(", ".join([link.name for link in self.links]))
        res += "Metadata = {}\n".format(", ".join([str(data) for data in self.metadata]))
        for node in self.links:
            res += str(node)
        return res


def get_integers(filepath):
    line = open(filepath, mode="r").readline()
    numbers = [int(val) for val in line.split(" ")]
    return numbers


def make_nodes(numbers, offset):
    if offset >= len(numbers):
        return
    len_nodes = numbers[offset]
    len_metadata = numbers[offset + 1]
    offset += 2
    node = TreeNode()
    for _ in range(0, len_nodes):
        child_node, offset = make_nodes(numbers, offset)
        node.add_link(child_node)
    for _ in range(0, len_metadata):
        node.add_metadata(numbers[offset])
        offset += 1
    return node, offset


numbers = get_integers("inputs/input08.txt")
node = make_nodes(numbers, 0)[0]
print(node.value())


def test():
    tn = TreeNode()
    tnb = TreeNode()
    tnc = TreeNode()
    tn.add_link(tnb)
    tn.add_link(tnc)
    tn.add_metadata(32)
    tn.add_metadata(64)
    tnb.add_metadata(2)
    print(tn)
    print(tnb)
    print(tnc)
    print(tn.metadata_sum())

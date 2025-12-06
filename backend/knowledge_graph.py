# knowledge_graph.py
import networkx as nx

class KG:
    def __init__(self):
        self.g = nx.Graph()

    def add_hospital(self, name, attrs=None):
        self.g.add_node(f"hospital:{name}", **(attrs or {}))

    def add_doctor(self, name, attrs=None):
        self.g.add_node(f"doctor:{name}", **(attrs or {}))

    def add_patient(self, pid, attrs=None):
        self.g.add_node(f"patient:{pid}", **(attrs or {}))

    def link(self, a, b, relation):
        self.g.add_edge(a, b, relation=relation)

    def is_doctor_of(self, doctor, patient):
        return self.g.has_edge(f"doctor:{doctor}", f"patient:{patient}")

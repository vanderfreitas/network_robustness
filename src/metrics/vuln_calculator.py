# -*- coding: utf-8 -*-

from igraph import *
import os


class GraphMaking:

    def __init__(self, flow):
        self.graph = None
        self.flow = flow
        self.contador = 0
        self.order = 0
        self.vuln = []
        self.ek = []


    def create_graph(self,g):

        self.graph = g
        self.order = self.graph.vcount()
        self.n = self.order

        self.vertices_list = g.vs['label']

    def global_efficiency(self, g):
        invcam = 0
        self.mencam = g.shortest_paths_dijkstra()
        for vertice in self.mencam:
            for caminho in vertice:
                if caminho != 0:
                    invcam += 1 / caminho
        eg = invcam / (self.n * (self.n - 1))
        if self.contador == 0:
            self.origi_efi = eg
        else:
            self.ek.append(eg)
        self.contador += 1
        return eg

    def vulnerability(self):

        eg = self.global_efficiency(self.graph)

        for i in range(0, self.order):
            g = self.graph.copy()
            del_list = []
            for target_vertex_id in range(0, self.order):
                try:
                    del_list.append(g.get_eid(i,target_vertex_id))
                except:
                    pass
            g.delete_edges(del_list)
            efi = self.global_efficiency(g)
            v = (eg - efi) / eg
            self.vuln.append(v)
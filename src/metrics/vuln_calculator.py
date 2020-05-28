# -*- coding: utf-8 -*-

from igraph import *
import os


class GraphMaking:

    def __init__(self, flow):
        self.graph = None
        self.flow = flow
        self.contador = 0
        self.order = 0
        self.infinities = []
        self.vuln = []
        self.weighted_vuln = []

        self.pop = 0
        self.ek = []
        self.infinities_weight = []

        for line in self.flow:
            self.pop += sum(line)


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


    def weighted_global_efficiency(self, g):
        invcam = 0
        pop = 0
        for lista in self.flow:
            for elemento in lista:
                pop += elemento
        self.mencam = g.shortest_paths_dijkstra()  # Função que retorna o menor caminho entre cada par de vértices do grafo
        # 'If' com o objetivo de manter 'n' constante (pois após remover um vértice n se torna n-1)
        for i, vertice in enumerate(self.mencam):  # itera para cada vertice de origem na lista de menores caminhos
            for j, caminho in enumerate(vertice):  # itera para cada destino do vertice de origem em questão
                if caminho != 0:
                    invcam += (1 / caminho) * self.flow[i][j]  # Acumula os valores de eficiencia associada a cada par de vértices

        eg = invcam / (self.n * (self.n - 1) * pop)
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

    def weighted_vulnerability(self):
        # Eficiencia com o vertice
        eg = self.weighted_global_efficiency(self.graph)
        # Eficiencia sem o vertice
        for i in range(0, self.order):
            #print("weighted vuln (" + str(i) + "/" + str(self.order) + ")")
            g = self.graph.copy()  # A cada iteração a varoável 'graf' receberá a cópia do grafo original
            del_list = []  # lista que conterá os ids das arestas do vértice 'i' que serão removidas.
            for target_vertex_id in range(0, self.order):
                try:
                    del_list.append(g.get_eid(i, target_vertex_id))  # função que captura o id da aresta pertencente ao par de vértices (i, target_vertex_id), e acrescenta na lista 'del_list'
                except:
                    pass  # caso o id não exista
            g.delete_edges(del_list)
            efi = self.weighted_global_efficiency(g)
            v_w = (eg - efi) / eg
            self.weighted_vuln.append(v_w)
            #print(v_w)
            #print('w_vuln' + ';' + str(i) + ';' + str(v_w))

    def isolation(self):
        for i in range(0,self.order):  # for de 0 até a quantidade de vértices, onde cada iteração representa uma rua que ficará inacessível a todas as outras.
            #print("isolation (" + str(i) + "/" + str(self.order) + ")")
            self.acumula_infinito = 0  # Variável que guardará a quantidade de infinitos após as arestas do vértice 'i' ser removida
            graph_copy = self.graph.copy()  # A cada iteração a varoável 'graf' receberá a cópia do grafo original
            del_list = []  # lista que conterá os ids das arestas do vértice 'i' que serão removidas.
            for target_vertex_id in range(0, self.order):
                try:
                    del_list.append(graph_copy.get_eid(i,target_vertex_id))  # função que captura o id da aresta pertencente ao par de vértices (i, target_vertex_id), e acrescenta na lista 'del_list'
                except:
                    pass  # caso o id não exista
            graph_copy.delete_edges(del_list)  # deleta as arestas contidas na lista 'del_list'
            self.mencam = graph_copy.shortest_paths_dijkstra()  # cria lista com todos os menores caminhos para de/para todos os vértices
            for vertice in self.mencam:  # itera para cada vertice de origem na lista de menores caminhos
                self.acumula_infinito += vertice.count(float('inf'))  # Guarda as ruas inacessiveis para um determinado vértice quando ele é removido
            self.infinities.append(self.acumula_infinito)  # lista que guarda em cada posição a quantidade de infinitos relacionados ao isolamento da rua 'i'.
            #print('isolation' + ';' + str(i) + ';' + str(self.acumula_infinito))

    def weighted_isolation(self):
        for i in range(0,self.order):  # for de 0 até a quantidade de vértices, onde cada iteração representa uma rua que ficará inacessível a todas as outras.
            #print("weighted isolation (" + str(i) + "/" + str(self.order) + ")")
            self.acumula_infinito = 0  # Variável que guardará a quantidade de infinitos após as arestas do vértice 'i' ser removida
            graph_copy = self.graph.copy()  # A cada iteração a varoável 'graf' receberá a cópia do grafo original
            del_list = []  # lista que conterá os ids das arestas do vértice 'i' que serão removidas.
            for target_vertex_id in range(0, self.order):
                try:
                    del_list.append(graph_copy.get_eid(i,target_vertex_id))  # função que captura o id da aresta pertencente ao par de vértices (i, target_vertex_id), e acrescenta na lista 'del_list'
                except:
                    pass  # caso o id não exista
            graph_copy.delete_edges(del_list)  # deleta as arestas contidas na lista 'del_list'
            self.mencam = graph_copy.shortest_paths_dijkstra()  # cria lista com todos os menores caminhos para de/para todos os vértices
            for ii, vertice in enumerate(self.mencam):  # itera para cada vertice de origem na lista de menores caminhos
                for j, path in enumerate(vertice):
                    if path==float('inf'):
                        self.acumula_infinito += (1*self.flow[ii][j])/self.pop
            self.infinities_weight.append(self.acumula_infinito)  # lista que guarda em cada posição a quantidade de infinitos relacionados ao isolamento da rua 'i'.
            #print(self.acumula_infinito)
            #print('w_isolation' + ';' + str(i) + ';' + str(self.acumula_infinito))
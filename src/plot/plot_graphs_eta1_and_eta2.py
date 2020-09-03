from matplotlib.artist import Artist
from igraph import BoundingBox, Graph, palettes
import string
import numpy as np


########### LOADING INPUT FILES ##############
import sys
sys.path.append('../')
from data_files import Input_files

in_files = Input_files('../../') 
codes = np.genfromtxt(in_files.get_codes_file_name())
f_matrix_original = np.genfromtxt(in_files.get_network_file_name(),delimiter=';')
##############################################

# convert codes to int
codes = codes.astype(int)


cities_coord = np.genfromtxt('../../input_data/cities_coord.csv',delimiter=',')


N = len(codes)


relative_path_in = '../../results/' + in_files.get_project_name() + '/robustness/'
relative_path = '../../results/'


data = np.genfromtxt('../../results/' + in_files.get_project_name() + '/metrics/avg_std.csv', delimiter=';') 

avg = data[0]
std = data[1]


print('PLOTTING THE MOBILITY NETWORKS')




class GraphArtist(Artist):
    """Matplotlib artist class that draws igraph graphs.

    Only Cairo-based backends are supported.
    """

    def __init__(self, graph, bbox, palette=None, *args, **kwds):
        """Constructs a graph artist that draws the given graph within
        the given bounding box.

        `graph` must be an instance of `igraph.Graph`.
        `bbox` must either be an instance of `igraph.drawing.BoundingBox`
        or a 4-tuple (`left`, `top`, `width`, `height`). The tuple
        will be passed on to the constructor of `BoundingBox`.
        `palette` is an igraph palette that is used to transform
        numeric color IDs to RGB values. If `None`, a default grayscale
        palette is used from igraph.

        All the remaining positional and keyword arguments are passed
        on intact to `igraph.Graph.__plot__`.
        """
        Artist.__init__(self)

        if not isinstance(graph, Graph):
            raise TypeError("expected igraph.Graph, got %r" % type(graph))

        self.graph = graph
        self.palette = palette or palettes["gray"]
        self.bbox = BoundingBox(bbox)
        self.args = args
        self.kwds = kwds

    def draw(self, renderer):
        from matplotlib.backends.backend_cairo import RendererCairo
        if not isinstance(renderer, RendererCairo):
            raise TypeError("graph plotting is supported only on Cairo backends")
        self.graph.__plot__(renderer.gc.ctx, self.bbox, self.palette, *self.args, **self.kwds)




import math

# Make Matplotlib use a Cairo backend
import matplotlib
matplotlib.use("cairo")
import matplotlib.pyplot as pyplot

import numpy as np
import igraph as ig


'''
Acre – Capital: Rio Branco.
Amapá – Capital: Macapá.
Amazonas – Capital: Manaus.
Pará – Capital: Belém.
Rondônia – Capital: Porto Velho.
Roraima – Capital: Boa Vista.
Tocantins – Capital: Palmas.
Alagoas – Capital: Maceió.
Bahia – Capital: Salvador.
Ceará – Capital: Fortaleza.
Maranhão – Capital: São Luís.
Paraíba – Capital: João Pessoa.
Pernambuco – Capital: Recife.
Piauí – Capital: Teresina.
Rio Grande do Norte – Capital: Natal.
Sergipe – Capital: Aracaju.
Goiás – Capital: Goiânia.
Mato Grosso – Capital: Cuiabá.
Mato Grosso do Sul – Capital: Campo Grande.
Distrito Federal – Capital: Brasília.
Espírito Santo – Capital: Vitória.
Minas Gerais – Capital: Belo Horizonte.
São Paulo – Capital: São Paulo.
Rio de Janeiro – Capital: Rio de Janeiro.
Paraná – Capital: Curitiba.
Rio Grande do Sul – Capital: Porto Alegre.
Santa Catarina – Capital: Florianópolis'''

capitals = np.array([1200401, 1600303, 1302603, 1501402,
            1100205, 1400100 ,1721000, 2704302, 2927408,
            2304400, 2111300, 2507507, 2611606, 2211001,
            2408102, 2800308, 5208707, 5103403, 5002704,
            5300108, 3205309, 3106200, 3550308, 3304557, 
            4106902, 4314902, 4205407])



fig, ax = pyplot.subplots(1, 2)
fig.set_size_inches(17,1*(16/2.0))

etas = ['eta1', 'eta2']
thresholds = [avg, avg+std]

for eta in range(2):


    thresh = thresholds[eta]

    A = f_matrix_original.copy()

    # Apply threshold
    for row in range(N):
        for col in range(N):
            if A[row][col] < thresh:
                A[row][col] = 0
            else:
                A[row][col] = 1


    # Removendo as cidades estrangeiras
    codes_ = codes[:-35]
    A = A[:-35,:-35]

    g = ig.Graph.Adjacency( A.tolist())
    N = g.vcount()

    # Convert to undirected graph
    g = g.as_undirected()

    N = len(codes_)

    for i in range(N):
        index = np.where(cities_coord[:,0] == int(codes_[i]))

        X = cities_coord[index[0][0],1]
        Y = cities_coord[index[0][0],2] * (-1)

        g.vs[i]["X"] = X
        g.vs[i]["Y"] = Y

        g.vs[i]["code"] = codes_[i]
        g.vs[i]["size"] = 5

    # capitals with bigger node
    for i in range(len(capitals)):
        index = np.where(codes_ == int(capitals[i]))

        g.vs[index[0][0]]["size"] = 12


    degrees = g.degree()
    to_delete = []


    for i in range(N):
        if(degrees[i] == 0):
            to_delete.append(i)


    g.delete_vertices(to_delete)


    degrees = g.degree()

    degrees = np.array(degrees)

    min_k = 1.0
    max_k = 29.3


    for i in range(g.vcount()):
        c = (degrees[i] - min_k) / (max_k - min_k)
        c = int(c * 255.0)
        if(c > 255):
            c = 255

        if(c < 10): #blue with some alpha variation
            g.vs[i]["color"] = "rgba(0, 0, 255,0.75)"
        else:
            g.vs[i]["color"] = "rgba(" + str( c ) + ", 0, 0,0.85)"

    # light gray edges
    g.es["color"] = "rgb(150, 150, 150)"


    layout = []
    for i in range(g.vcount()):
        layout.append( (g.vs[i]["X"],g.vs[i]["Y"]) )


    visual_style = {}
    visual_style["vertex_size"] = g.vs["size"]
    visual_style["edge_width"] = 1
    #visual_style["vertex_label"] = g.vs["label"]
    visual_style["layout"] = layout
    #visual_style["bbox"] = (1000, 1000)
    visual_style["margin"] = 30

    '''
    # Draw the graph over the plot
    # Two points to note here:
    # 1) we add the graph to the axes, not to the figure. This is because
    #    the axes are always drawn on top of everything in a matplotlib
    #    figure, and we want the graph to be on top of the axes.
    # 2) we set the z-order of the graph to infinity to ensure that it is
    #    drawn above all the curves drawn by the axes object itself.
    g = Graph.GRG(100, 0.2)'''
    graph_artist = GraphArtist(g, bbox=(0+eta*650,0,600+eta*600,600),   **visual_style)
    ax[eta].artists.append(graph_artist)
    ax[eta].axis('off')


    ax[eta].text(-0.1, 1.1, string.ascii_uppercase[eta], transform=ax[eta].transAxes, size=30) #, weight='bold')

# Save the figure
fig.savefig(relative_path + 'f_vs_Pinfty.pdf')

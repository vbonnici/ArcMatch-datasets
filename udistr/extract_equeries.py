#!/usr/bin/python3

import sys
import re
import math
import random
import copy

print(sys.argv)

i_net = sys.argv[1]				#graph file, node-labeled RI format, directed
i_directed = sys.argv[2]			#true [false]
i_nof_subgraphs = int(sys.argv[3])		#integer > 0
i_nof_nodes = int(sys.argv[4])			#integer > 0  == n
i_perc_edges = float(sys.argv[5])		#[0.0,1.0] w.r.t n^2
i_o_prefix = sys.argv[6]			#path... odir/name_*  0.gfd, 1.gfd
i_o_suffix = sys.argv[7]			#.efgd

random.seed(i_nof_subgraphs)

if i_directed == 'false':
    i_directed = False
else:
    i_directed = True

if i_perc_edges > 1.0:
    i_perc_edges = 1.0

if i_directed:
    if i_perc_edges <= 0.0:
        i_perc_edges = (i_nof_nodes - 1) / (i_nof_nodes * i_nof_nodes)
    i_nof_edges = math.ceil(i_perc_edges * (i_nof_nodes * i_nof_nodes))
    if i_nof_edges < (i_nof_nodes - 1):
        i_nof_edges = (i_nof_nodes - 1)
else:
    if i_perc_edges <= 0.0:
        i_perc_edges = (i_nof_nodes - 1) / ((i_nof_nodes * (i_nof_nodes - 1)) / 2)
    i_nof_edges = math.ceil(i_perc_edges * ((i_nof_nodes * (i_nof_nodes - 1)) / 2))
    if i_nof_edges < (i_nof_nodes - 1):
        i_nof_edges = (i_nof_nodes - 1)

print('input network', i_net)
print('is directed', i_directed)
print('number of subgraphs', i_nof_subgraphs)
print('number of subgraph nodes',i_nof_nodes)
print('percentage of subgraph edges', i_perc_edges)
print('required edges', i_nof_edges)
print('output prefix', i_o_prefix)

max_nof_trials = 100


class graph_t:
    def __init__(self, name, nof_nodes):
        self.name = name
        self.node_labels = [None for i in range(nof_nodes)]
        self.o_edges = dict() # [e_s] -> {  [e_t]->label  }
        self.i_edges = dict() # [e_t] -> {  [e_s]->label  }
        self.neighs = dict()
        for i in range(nof_nodes):
            self.neighs[i] = set()
        #self.edges = [ [False for i in range(nof_nodes)] for i in range(nof_nodes) ]
        #self.edge_labels = [ [None for i in range(nof_nodes)] for i in range(nof_nodes) ]
    def set_node_label(self, node_i, label):
        self.node_labels[node_i] = label
    def get_node_label(self, node_i):
        return self.node_labels[node_i]
    def set_edge(self, source_i, target_i, label):
        if source_i not in self.o_edges:
            self.o_edges[source_i] = dict()
        self.o_edges[source_i][target_i] = label
        if target_i not in self.i_edges:
            self.i_edges[target_i] = dict()
        self.i_edges[target_i][source_i] = label
        
        self.neighs[source_i].add(target_i)
        self.neighs[target_i].add(source_i)
        
    def get_edge(self, source_i, target_i):
        if (source_i in self.o_edges) and (target_i in self.o_edges[source_i]):
            return True, self.o_edges[source_i][target_i]
        else:
            return False, None
    def get_edge_label(self, source_i, target_i):
        #if (source_i in self.o_edges) and (target_i in self.o_edges[source_i]):
        if source_i in self.o_edges:
            return self.o_edges[source_i].get(target_i, None)
        else:
            return None
    def is_edge(self, source_i, target_i):
        #if (source_i in self.o_edges) and (target_i in self.o_edges[source_i]):
        if source_i in self.o_edges:
            if target_i in self.o_edges[source_i]:
                return True
        return False
    def freeze_neighs(self):
        for i in range(self.nof_nodes()):
            self.neighs[i] = sorted(self.neighs[i])
    def get_neighs(self, node_i):
        return copy.deepcopy( self.neighs[node_i])
        #print(node_i, (node_i in self.o_edges), (node_i in self.i_edges))
        # a = set()
        # b = set()
        # if node_i in self.o_edges:
        #     a = self.o_edges[node_i].keys()
        # if node_i in self.i_edges:
        #     b = self.i_edges[node_i].keys()
        # return list(a | b)
        # if node_i in self.o_edges:
        #     if node_i in self.i_edges:
        #         return list(self.o_edges[node_i].keys() & self.i_edges[node_i].keys())
        #     else:
        #         return list(self.o_edges[node_i].keys())
        # else:
        #     return []
    def get_out_neighs(self, node_i):
        if node_i in self.o_edges:
            return list(self.o_edges[node_i].keys())
        return []
    def get_in_neighs(self, node_i):
        if node_i in self.i_edges:
            return list(self.i_edges[node_i].keys())
        return []
    def nof_nodes(self):
        return len(self.node_labels)
    def nof_edges(self):
        c = 0
        for k in self.o_edges.keys():
            c += len(self.o_edges[k])
            #for i in self.o_edges[k].keys():
                #if i:
                #c += 1
        return c
    def get_component_nodes(self, min_nodes):
        to_return = set()
        nof_nodes = self.nof_nodes()
        visited = [False for i in range(nof_nodes)]
        c_visited = 0
        print(len(visited))
        i_s = -1
        while i_s < nof_nodes:
            c_comp = list()
            ci = 0
            while i_s < nof_nodes - 1:
                i_s += 1
                if i_s not in visited:
                    c_comp.append(i_s)
                    visited[i_s] = True
                    c_visited += 1
                    break
            while (ci < len(c_comp)) and (c_visited < nof_nodes):
                for n in self.get_neighs(c_comp[ci]):
                    if visited[n] == False:
                        c_comp.append(n)
                        visited[n] = True
                        c_visited += 1
                ci += 1
            #print('|c_comp|',len(c_comp))
            if len(c_comp) >= min_nodes:
                to_return = to_return | set(c_comp)
            #print('|visited|', len(visited))
        #print('component length distribution')
        #for k,v in sorted(c_distr.items()):
        #    print(k,v)
        return to_return
    def get_mindegree_nodes(self, mindegree):
        to_return = list()
        for i in self.nof_nodes():
            if len(self.get_neighs(i)) >= mindegree:
                to_return.append(i)
        return to_return

def read_graph(ifile, is_directed):
    iff = open(ifile, 'r')
    name = iff.readline().strip()
    nof_nodes = int(iff.readline())
    g  = graph_t(name, nof_nodes)
    for i in range(nof_nodes):
        label = iff.readline().strip()
        g.set_node_label(i, label)
    nof_edges = int(iff.readline())
    p = re.compile('\s+')
    for i in range(nof_edges):
        cc = p.split(iff.readline().strip())
        label = None
        if len(cc) > 2:
            label = cc[2]
        g.set_edge(int(cc[0]), int(cc[1]), label)
        if not is_directed:
            g.set_edge(int(cc[1]), int(cc[0]), label)   
    return g

def write_graph(ofile, g):
    off = open(ofile, 'w')
    off.write(g.name.strip() + '\n')
    off.write(str(g.nof_nodes()) + '\n')
    for i in range(g.nof_nodes()):
        off.write(g.get_node_label(i).strip() + '\n')
    off.write(str(g.nof_edges()) + '\n')
    for i in range(g.nof_nodes()):
        for j in range(g.nof_nodes()):
            a,l = g.get_edge(i,j)
            #print(i,j,a,l)
            if a:
                if l:
                    off.write(str(i) +' '+ str(j) +' '+ str(l) +'\n')
                else:
                    off.write(str(i) +' '+ str(j) + '\n')
    off.flush()
    off.close()

def extract_subgraph(inet, available_nodes, name, nof_nodes, nof_edges, is_directed):
    """
    It works on directed graphs, and extract directed subgraphs
    """
    
    #s_nodes = [ random.randint(0, inet.nof_nodes() - 1) ]
    s_nodes = [   available_nodes[  random.randint(0, len(available_nodes) - 1)   ]   ]
    s_neighs = inet.get_neighs(s_nodes[0])
    
    #print(0,s_nodes[0],inet.get_neighs(s_nodes[0]))
    
    # extract adjacent nodes
    #print(s_nodes, s_neighs)
    for i in range(nof_nodes - 1):
        #print(i, nof_nodes)
        if len(s_neighs) == 0:
            return None, None
        a = random.choice(s_neighs)
        s_nodes.append(a)
        s_neighs.remove(a)
        #print(i,a,inet.get_neighs(a))
        for n in inet.get_neighs(a):
            if (n not in s_nodes) and (n not in s_neighs):
                s_neighs.append(n)
        #print(s_nodes, s_neighs)
        
    #print(s_nodes, s_neighs)
    s_edges = set()
    
    
    
    # create a connected subgraph
    for i in range(len(s_nodes) - 1):
        #print(s_nodes[i], inet.get_neighs(s_nodes[i]), s_nodes)
        p = random.choice(list(set(inet.get_neighs(s_nodes[i])) & (set(s_nodes) - {s_nodes[i]} )))
        if is_directed:
            if inet.is_edge(s_nodes[i],p):
                s_edges.add( (s_nodes[i],p) )
            else:
                s_edges.add( (p,s_nodes[i]) )
        else:
            s_edges.add( (s_nodes[i],p) )
            s_edges.add( (p,s_nodes[i]) )
    #print(s_edges)
    
    # extract other edges
    s_neighs = list()
    s_nodes = sorted(s_nodes)
    for i in range(len(s_nodes) - 1):
        for j in range(i + 1, len(s_nodes) - 1):
            if inet.is_edge(s_nodes[i], s_nodes[j]) and (s_nodes[i],s_nodes[j]) not in s_edges:
                s_neighs.append( (s_nodes[i],s_nodes[j]) )
            if inet.is_edge(s_nodes[j],s_nodes[i]) and (s_nodes[j],s_nodes[i]) not in s_edges:
                s_neighs.append( (s_nodes[j],s_nodes[i]) )
    #print(s_neighs)
    
    #print('edges to choose', nof_edges - len(s_edges), nof_edges, len(s_edges))
    to = nof_edges - len(s_edges)
    if to < 0:
        to = 0
    #for i in range( nof_edges - len(s_edges)  ):
    for i in range( to ):
        if len(s_neighs) == 0:
            break
        e = random.choice(s_neighs)
        s_edges.add(e)
        s_neighs.remove(e)
        
        if not is_directed:
            s_edges.add( (e[1],e[0]) )
            s_neighs.remove( (e[1],e[0]) )
        
    # create the new graph
    random.shuffle(s_nodes)
    #print('chosen nodes', s_nodes)
    nmap = { s_nodes[i] : i for i in range(len(s_nodes))  }
    #print('nmap', nmap)
    
    subnet = graph_t(name, len(s_nodes))
    for i in range(len(s_nodes)):
        subnet.set_node_label(i,  inet.get_node_label(s_nodes[i]))
    for e in s_edges:
        #print('mapping edge', e)
        subnet.set_edge(  nmap[e[0]], nmap[e[1]], inet.get_edge_label(e[0], e[1]) )
    #print(len(s_edges))
    return subnet, s_nodes




print('-'*80)
print('reading network...')
inet = read_graph(i_net, i_directed)
print('freezing...')
inet.freeze_neighs()
print('info...')
print('nodes', inet.nof_nodes())
print('edges', inet.nof_edges())



# print('connected components...')
# av_nodes = list(inet.get_component_nodes(i_nof_nodes))
# if len(av_nodes) < i_nof_nodes:
#     print('there is not a connect component big enought', len(av_nodes))
#     quit()

# print('min degree nodes',i_nof_nodes,'...')
# av_nodes = list(inet.get_mindegree_nodes(i_nof_nodes))
# if len(av_nodes) < i_nof_nodes:
#     print('there is not a connect component big enought', len(av_nodes))
#     quit()

av_nodes = [i for i in range(inet.nof_nodes())]

e_distr = dict()

for i in range(i_nof_subgraphs):
    print('-'*40)
    
    min_edges = i_nof_nodes - 1
    c_edges = random.randint(min_edges, i_nof_edges)
    
    #sg, nmap = extract_subgraph(inet, av_nodes, inet.name +'_sub_'+ str(i), i_nof_nodes, i_nof_edges, i_directed)
    print('subgraph',i)
    sg, nmap = extract_subgraph(inet, av_nodes, inet.name +'_sub_'+ str(i), i_nof_nodes, c_edges, i_directed)
    
    # if sg != None:
    #     print('writing...')
    #     e_distr[sg.nof_edges()] = e_distr.get(sg.nof_edges(), 0) + 1
    #     write_graph(i_o_prefix + '_sub_'+str(i)+'.gfd', sg)
    
    t = 0
    while (sg == None) and (t < max_nof_trials):
        sg, nmap = extract_subgraph(inet, av_nodes, inet.name +'_sub_'+ str(i), i_nof_nodes, c_edges, i_directed)
        t += 1
    
    print(t, max_nof_trials, sg)
    if t < max_nof_trials:
        e_distr[sg.nof_edges()] = e_distr.get(sg.nof_edges(), 0) + 1
        print('writing...')
        write_graph(i_o_prefix + '_sub_'+str(i)+i_o_suffix, sg)
    else:
        print('reached max nof trials')
    # 
    # # print(sg.name)
    # # print(sg.nof_nodes(), sg.nof_edges())
    # # print(nmap)
    #print('writing...')
    #write_graph(i_o_prefix + '_sub_'+str(i)+'.gfd', sg)

print('nof_edges distribution')
for k,v in sorted(e_distr.items()):
    print(k,v)
print('-'*80)

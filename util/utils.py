# -*-coding:utf-8-*-
import pandas as pd

def load_data(path_1, path_2):
    file_1 = open(path_1)
    cmt_list = []
    for line in file_1.readlines():
        temp_list = []
        curLine = line.strip().split('	')
        for i in range(len(curLine)):
            temp_list.append(curLine[i])
        cmt_list.append(temp_list)
    file_1.close()

    file_2 = open(path_2)
    edge_list = []
    for line in file_2.readlines():
        temp_list = []
        curLine = line.strip().split('	')
        for i in range(len(curLine)):
            temp_list.append(curLine[i])
        edge_list.append(temp_list)
    file_2.close()

    return cmt_list, edge_list

# output new_graph
def outputEdges(edges, path):
    name = ['id_1','id_2']
    instance = pd.DataFrame(columns=name, data=edges)
    instance.to_csv(path,encoding='utf-8', index=False)

# output new_cmts
def outputCmts(cmts, path):
    f = open(path, 'w')
    f.write(str(cmts))
    f.close()

# output information of the newly constructed dataset
def outputReadme(n_nodes, n_edges, n_cmts, time, author, path):
    f = open(path, 'w')
    info = 'number of nodes:' + n_nodes + '\nnumber of edges:' + n_edges +\
           '\nnumber of communties:' + n_cmts + '\ntime:' + time + '\nauthor:'+ author
    f.write(info)
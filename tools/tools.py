# -*-coding:utf-8-*-
from tqdm import tqdm
import numpy as np
import scipy.sparse as sp
import scipy.io



# find the highest density community
def findStartCmt(cmts, size):
    Id = 0
    maxLength = -1
    for i in range(len(cmts)):
        if len(cmts[i]) >= size[0] and len(cmts[i]) <= size[1]:
            if len(cmts[i]) > maxLength:
                maxLength = len(cmts[i])
                Id = i
    return Id

def updateNodes(ori_nodes, queue_nodes, new_nodes):
    for i in range(len(new_nodes)):
        if new_nodes[i] not in ori_nodes:
            ori_nodes.append(new_nodes[i])
            queue_nodes.put(new_nodes[i])

def findRelatedCmt(node, cmt, gt_cmtId, size):
    Id = 0
    isFound = False
    for id in range(len(cmt)):
        if id not in gt_cmtId:
            if node in cmt[id] and (len(cmt[id]) < size[1] and len(cmt[id]) > size[0]):
                Id = id
                isFound = True
    return Id, isFound

def findNeighborNode(cur_node, edges):
    degree_list = []
    neighbor_list = []
    for edge in edges:
        if edge[0] == cur_node:
            neighbor_list.append(edge[1])
        elif edge[1] == cur_node:
            neighbor_list.append(edge[0])
    maxId = -1
    for i in range(len(neighbor_list)):
        cur_deg = 0
        for edge_ in edges:
            if edge_[0] == neighbor_list[i] or edge_[1] == neighbor_list[i]:
                cur_deg += 1
        if cur_deg > maxId:
            maxId = i
        degree_list.append(cur_deg)
    return neighbor_list[maxId]

def constructEdges(nodes, edges):
    new_edges = []
    for edge in tqdm(edges):
        if edge[0] in nodes and edge[1] in nodes:
            new_edges.append(edge)
    return new_edges

def findIndex(node, node_list):
    index = -1
    for n in range(len(node_list)):
        if node == node_list[n]:
            index = n
            break
    return index

def constructNewEdges(nodes,edges):
    len_node = len(nodes)
    new_edges = []
    index = [i for i in range(len_node)]
    # iterate edges
    for edge in tqdm(edges):
        e1 = findIndex(edge[0], nodes)
        e2 = findIndex(edge[1], nodes)
        new_edges.append([e1, e2])
    return new_edges

def constructNewCmts(gt_cmt_id, ori_cmts, node_list):
    len_cmt = len(gt_cmt_id)
    cmt_dict= dict()
    for i in range(len_cmt):
        cur_cmt = ori_cmts[gt_cmt_id[i]]
        new_cmt = []
        for j in range(len(cur_cmt)):
            new_cmt.append(findIndex(cur_cmt[j], node_list))
        t = {i:new_cmt}
        cmt_dict.update(t)
    return cmt_dict

def constructMatrix(edges_list, length, path):
    edges = np.array(edges_list)
    adj = sp.coo_matrix((np.ones(edges.shape[0]), (edges[:, 0], edges[:, 1])),
                        shape=(length, length),
                        dtype=np.double)
    adj = adj + adj.T.multiply(adj.T > adj) - adj.multiply(adj.T > adj)
    scipy.io.savemat(path, mdict={'adj': adj})
# -*-coding:utf-8-*-
from util import utils
from tools import tools
import queue
import time
import pandas as pd
dataset = 'Amazon'
author = 'zhuye'
cmt_data = './data/com-amazon-cmty.txt'
ungraph_data = './data/com-amazon-ungraph.txt'
outputEdges_path = './output/amazon-ungraph_3.csv'
outputCmts_path = './output/amazon-cmt_3.txt'
outputInfo_path = './output/amazon-readme_3.txt'
outputMatrix_path = './output/amazon-matrix_3.mat'

# variables
set_num = 10000
cmt_size = [100,600]
nodes_list = []
nodes_queue = queue.Queue(maxsize=0)
gt_cmtId = []

start_time = time.time()

# load data
ori_cmts, ori_edges = utils.load_data(cmt_data,ungraph_data)
# find the specific community to start, the condition of this community can be different!
startCmt_id = tools.findStartCmt(ori_cmts, [440,459])
# update nodes list, update gt_cmt list
tools.updateNodes(nodes_list, nodes_queue, ori_cmts[startCmt_id])
gt_cmtId.append(startCmt_id)

# begin to iterate all the communities
while len(nodes_list) < set_num:
    cur_node = nodes_queue.get()
    # via overlap nodes
    olap_cmt_id, isFound = tools.findRelatedCmt(cur_node, ori_cmts, gt_cmtId, cmt_size)
    # find it or not: found, update node list and gt_cmt list
    if isFound == True:
        tools.updateNodes(nodes_list, nodes_queue, ori_cmts[olap_cmt_id])
        gt_cmtId.append(olap_cmt_id)
    else:
        nbor_node = tools.findNeighborNode(cur_node, ori_edges)
        nbor_cmt_id, isFound_ = tools.findRelatedCmt(nbor_node, ori_cmts, gt_cmtId, cmt_size)
        if isFound_ == True:
            tools.updateNodes(nodes_list, nodes_queue, ori_cmts[nbor_cmt_id])
            gt_cmtId.append(nbor_cmt_id)
    print("current number of the nodes:" + str(len(nodes_list)) + "/10000")

# construct gt_edges
gt_edges = tools.constructEdges(nodes_list, ori_edges)

# construct new_gt_edges
new_gt_edges = tools.constructNewEdges(nodes_list, gt_edges)
utils.outputEdges(new_gt_edges, outputEdges_path)

# construct new_gt_cmts
new_gt_cmts = tools.constructNewCmts(gt_cmtId, ori_cmts, nodes_list)
utils.outputCmts(new_gt_cmts, outputCmts_path)

# construct matrix.mat via new_gt_edges
tools.constructMatrix(new_gt_edges, len(nodes_list), outputMatrix_path)


end_time = time.time()
total_time = (end_time - start_time) / 60

# number of the nodes, number of the edges, number of the cmts, sampling time, author
utils.outputReadme(str(len(nodes_list)), str(len(gt_edges)), str(len(gt_cmtId)), str(total_time), author, outputInfo_path)



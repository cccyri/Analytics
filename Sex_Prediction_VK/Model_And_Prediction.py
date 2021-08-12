import torch
import os
import torch.nn as nn
import torch.nn.functional as F
from dgl.nn.pytorch import GraphConv
import numpy as np

from load_data_2 import MiptFpmiDataset

dataset = MiptFpmiDataset()
graph = dataset[0]


class GCN(nn.Module):
    def __init__(self, in_feats, h_feats, num_classes):
        super(GCN, self).__init__()
        self.conv1 = GraphConv(in_feats, h_feats, allow_zero_in_degree=True)
        self.conv2 = GraphConv(h_feats, num_classes, allow_zero_in_degree=True)

    def forward(self, g, in_feat):
        h = self.conv1(g, in_feat)
        h = F.relu(h)
        h = self.conv2(g, h)
        return h

class Train():

    val = 0

    def train(graph, net):

        inputs = graph.ndata['sex']
        labeled_nodes = graph.train_nodes # вершины - участнки у которых известен пол
        labels = graph.train_labels  # значения пола
        print(labels)

        optimizer = torch.optim.Adam(net.parameters(), lr=0.01) #itertools.chain(net.parameters(), embed.parameters()
        all_logits = []
        for epoch in range(200):
            logits = net(graph, inputs)
            # print(len(logits))
            # we save the logits for visualization later
            all_logits.append(logits.detach())
            logp = F.log_softmax(logits, 1)
            # print(len(logp))
            if epoch == 199:
                logp_1 = logp.detach().numpy()
                Train.val = logp_1

            loss = F.nll_loss(logp[labeled_nodes], labels) # we only compute loss for labeled nodes

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            print('Epoch %d | Loss: %.4f' % (epoch, loss.item()))

def test(graph, a): # выводит точность нейросети на тестовом наборе
    test_nodes = graph.test_nodes.numpy()
    test_labels = graph.test_labels.numpy()

    j = 0
    err_cnt = 0 # ошибочные предсказания
    right_cnt = 0 # верные предсказания
    for i in test_nodes:
        if a[i][0] > a[i][1]:
            if test_labels[j] == 0:
                right_cnt += 1
                j += 1
            else:
                err_cnt += 1
                j += 1
        elif a[i][0] < a[i][1]:
            if test_labels[j] == 1:
                right_cnt += 1
                j += 1
            else:
                err_cnt += 1
                j += 1

    kpd = (float(right_cnt / (right_cnt + err_cnt))) * 100
    print(kpd) # d #

def predict(graph, a): # предсказывает пол пользователя, которые его не указал
    nosex_list = graph.nosex_list.numpy()
    for i in nosex_list:
        if a[i][0] > a[i][1]:
            print(str(i) + ' is woman')
        elif a[i][0] < a[i][1]:
            print(str(i) + ' is man')


model = GCN(graph.ndata['sex'].shape[1], 16, 2)
Train.train(graph, model)
a = Train.val
test(graph, a)
predict(graph, a)



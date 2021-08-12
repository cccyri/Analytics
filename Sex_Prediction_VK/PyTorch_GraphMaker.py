import dgl
from dgl.data import DGLDataset
import torch
import os
import pandas as pd
import numpy as np


class MiptFpmiDataset(DGLDataset):
    def __init__(self):
        super().__init__(name='miptfpmi')

    def process(self):

        edges_data = pd.read_csv(r'C:\Users\CCCYRI\Downloads\data_2.csv')
        nodes_data = pd.read_csv(r'C:\Users\CCCYRI\Downloads\users_sex.csv')

        vec1 = nodes_data['Man'].to_numpy()
        vec2 = nodes_data['Woman'].to_numpy()
        vec3 = nodes_data['NoSex'].to_numpy()

        vector = vec1
        vector = np.vstack([vector, vec2])
        vector = np.vstack([vector, vec3])

        vector = vector.transpose() # вектор признаков

        train_nodes = list() # набор id вершин для обучения--
        train_labels = list() # значение в вершине (муж/жен)
        nosex_list = list() # список id вершин с неуказанным полом
        test_nodes = list() # набор id вершин для тестирования
        test_labels = list() # значение в вершине (муж/жен)

        for i in range(vector.shape[0]):

            if len(train_nodes) < 4000: # набор для обучения
                if vector[i][2] == 1:
                    nosex_list.append(i) # номера позиций кортежей без пола
                    print(i)
                elif vector[i][0] == 1:
                    train_nodes.append(i)
                    train_labels.append(1) # мужчина
                elif vector[i][1] == 1:
                    train_nodes.append(i)
                    train_labels.append(0) # женщина

            else:
                if vector[i][2] == 1:
                    nosex_list.append(i) # номера позиций кортежей без пола
                elif vector[i][0] == 1:
                    test_nodes.append(i)
                    test_labels.append(1) # мужчина
                elif vector[i][1] == 1:
                    test_nodes.append(i)
                    test_labels.append(0) # женщина

        train_nodes = pd.Series(train_nodes)
        train_labels = pd.Series(train_labels)
        nosex_list = pd.Series(nosex_list)
        test_nodes = pd.Series(test_nodes)
        test_labels = pd.Series(test_labels)

        train_nodes = torch.from_numpy(train_nodes.to_numpy())
        train_labels = torch.from_numpy(train_labels.to_numpy())
        nosex_list = torch.from_numpy(nosex_list.to_numpy())
        test_nodes = torch.from_numpy(test_nodes.to_numpy())
        test_labels = torch.from_numpy(test_labels.to_numpy())

        node_particulars_sex = torch.from_numpy(vector)
        #node_particulars_sex = torch.from_numpy(nodes_data['Sex'].astype('category').cat.codes.to_numpy())
        edges_src = torch.from_numpy(edges_data['Src'].to_numpy())
        edges_dst = torch.from_numpy(edges_data['Dst'].to_numpy())
        edge_features = torch.from_numpy(edges_data['Weight'].to_numpy())

        self.graph = dgl.graph((edges_src, edges_dst), num_nodes=nodes_data.shape[0])
        self.graph.ndata['sex'] = node_particulars_sex
        self.graph.edata['weight'] = edge_features

        self.graph.train_nodes = train_nodes
        self.graph.train_labels = train_labels
        self.graph.nosex_list = nosex_list
        self.graph.test_nodes = test_nodes
        self.graph.test_labels = test_labels

        n_nodes = nodes_data.shape[0]
        n_train = int(n_nodes * 0.6)
        n_val = int(n_nodes * 0.2)
        train_mask = torch.zeros(n_nodes, dtype=torch.bool)
        val_mask = torch.zeros(n_nodes, dtype=torch.bool)
        test_mask = torch.zeros(n_nodes, dtype=torch.bool)
        train_mask[:n_train] = True
        val_mask[n_train:n_train + n_val] = True
        test_mask[n_train + n_val:] = True
        self.graph.ndata['train_mask'] = train_mask
        self.graph.ndata['val_mask'] = val_mask
        self.graph.ndata['test_mask'] = test_mask

    def __getitem__(self, i):
        return self.graph

    def __len__(self):
        return 1

dataset = MiptFpmiDataset()
graph = dataset[0]

print(graph)
import os
import numpy as np
import pandas as pd
import networkx as nx
from collections import Counter
import random

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# files = os.listdir("input")
# print(files)

# file_name = 'KB.csv'
# data_parts = pd.read_csv(file_name)
# print(data_parts.columns)


def add_nodes(G, df, col, type_name):
    """Add entities to G from the 'col' column of the 'df' DataFrame. The new nodes are annotated with 'type_name' label."""
    nodes = list(df[~df[col].isnull()][col].unique())
    G.add_nodes_from([(n, dict(type=type_name)) for n in nodes])
    print("Nodes (%s,%s) were added" % (col, type_name))


def add_links(G, df, col1, col2, relation):
    """Add links to G from the 'df' DataFrame. The new edges are annotated with 'type_name' label."""
    df_tmp = df[(~df[col1].isnull()) & (~df[col2].isnull()) & (~df[relation].isnull())]
    links = list(zip(df_tmp[col1], df_tmp[col2], df_tmp[relation]))
    G.add_edges_from([(src, trg, dict(type=rel)) for src, trg, rel in links])
    print("Edges (%s->%s,%s) were added" % (col1, col2, relation))


# add_nodes(G, data_parts, "Resto", "restaurant")
# add_nodes(G, data_parts, "Resto_Result", "resto_result")
# add_links(G, data_parts, "Resto", "Resto_Result", "Resto_Relation")

# nx.write_gpickle(G, "KB.gpickle")
G = nx.read_gpickle(ROOT_DIR + "/KB.gpickle")
nodes = list(G.nodes)
edges = nx.get_edge_attributes(G, "type")
relations = [
    "R_location",
    "R_number",
    "R_rating",
    "R_address",
    "R_price",
    "R_cuisine",
    "R_phone",
]
predicates = [
    "vietnamese",
    "beijing",
    "six",
    "spanish",
    "korean",
    "seoul",
    "rome",
    "moderate",
    "london",
    "phone",
    "tokyo",
    "bombay",
    "cheap",
    "thai",
    "madrid",
    "1",
    "japanese",
    "7",
    "6",
    "paris",
    "address",
    "cantonese",
    "8",
    "hanoi",
    "british",
    "italian",
    "eight",
    "indian",
    "5",
    "bangkok",
    "2",
    "3",
    "4",
    "expensive",
    "two",
    "french",
    "four",
]
subjects_predicates = list(edges.keys())


def getCommonTermsIntersection(request):
    arrayOfsets = []
    for reqWord in request.split(" "):
        if reqWord in predicates:
            arrayOfsets.append(
                [word[0] for word in subjects_predicates if word[1] == reqWord]
            )

    if len(arrayOfsets) > 0:
        commonElements = arrayOfsets[0]
        for arrSet in arrayOfsets:
            commonElements = list(set(arrSet).intersection(commonElements))
        return commonElements
    else:
        return ""
    # request = ' dsadsad dsa a italian rome hi cheap 4 hfds fsdfjk sfdkf sdf k'


def getCommonTermsUnion(request):
    arrayOfsets = []
    for reqWord in request.split(" "):
        if reqWord in predicates:
            arrayOfsets.append(
                [word[0] for word in subjects_predicates if word[1] == reqWord]
            )

    if len(arrayOfsets) > 0:
        commonElements = arrayOfsets[0]
        for arrSet in arrayOfsets:
            commonElements = list(set(arrSet).union(commonElements))
        return commonElements
    else:
        return ""


# request = " dsadsad dsa a italian rome 4"
# print(getCommonTermsUnion(request))


# predicates = set()

# for val in edges.keys():
#     # print(val)
#     predicates.add(val[1])

# print(predicates[0])
# # print(random.choice(subjects_predicates))


# commonElements = list(set(romeRestaurants).intersection(italianRestaurants))
# print(arrayOfsets[1])

# romeRestaurants = [word[0] for word in subjects_predicates if word[1] == "address" ]
# italianRestaurants = [word[0] for word in subjects_predicates if word[1] == "italian" ]


# for word in request.split(' '):


# print(edges[('resto_seoul_cheap_korean_1stars', 'resto_seoul_cheap_korean_1stars_phone')])

# edgesSet = set()


# print(random.choices(nodes, k =10))
# print('***********************')
# print(type(edges))
# for key, value in edges.items():
# Iterate over key/value pairs in dict and print them
#     print(key)


# print(len(nodes))


# ########################## Create a new Dialogues with history ##########################
# allDialoguesWithHistory = createDialogueWithHistory(allDialogues)
# ########################## Print a random sample for comparison ##########################
# checkSample()
# ########################## Write a dialogue to a path ##########################
# writeToFile(targetPath,allDialoguesWithHistory)


# ########################## Helper Functions #########################
# randomDialogue = random.choice(allDialogues)
# for i in range(len(randomDialogue)):
#     print(i,": ", randomDialogue[i] ,"\n")

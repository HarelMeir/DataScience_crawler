import requests
import random
import lxml.html
from cityCrawler import cityCrawler
import numpy as np




# choose random vertex.
def random_vertex(link_dic, page_ranks, vertexes_list, numIters):
    vertex = random.choice(vertexes_list)
    page_ranks[vertex] += 1
    numIters -= 1
    return vertex, numIters

# if teleport == True
def teleport_on(links_dic, page_ranks, vertexes_list, numIters, flags):
    vertex, numIters = random_vertex(links_dic, page_ranks, vertexes_list, numIters)
    # if flag is on -> choose random vertex. else -> follow the link.
    while numIters > 0:
        flag = np.random.choice(flags, p=[0.2, 0.8])
        links = links_dic[vertex]
        if flag == 'on' or len(links) <= 0:
            vertex, numIters = random_vertex(links_dic, page_ranks, vertexes_list, numIters)
        else:
            vertex = random.choice(links)
            page_ranks[vertex] += 1
            numIters -= 1
    return page_ranks


# if teleport == False
def teleport_off(links_dic, page_ranks, vertexes_list, numIters):
    # choose a vertex randomly, and updates its
    vertex, numIters =  random_vertex(links_dic, page_ranks, vertexes_list, numIters)

    # the proccess numIters times.
    while numIters > 0:
        # if they is a link to other vertex from the current, follow the link.
        links = links_dic[vertex]
        if len(links) > 0:
            vertex = random.choice(links)
            page_ranks[vertex] += 1
            numIters -= 1
        # else choose randomly different vertex, and continue the process.
        else:
            vertex, numIters = random_vertex(links_dic, page_ranks, vertexes_list, numIters)
        # update the vertex data.
    return page_ranks




def cityRank(listOfPairs, numIters, teleports):

    vertexes = set()
    divider = numIters
    # getting the vertexes -> unique links.
    for x, y in listOfPairs:
        vertexes.add(x)
        vertexes.add(y)

    # initializing dictionary for the links.
    links_dic = {}
    page_ranks = {}

    # initalize the dictionaries.
    for ver in vertexes:
        links_dic[ver] = []
        page_ranks[ver] = 0
    # setting a dictionary for the links
    for x, y in listOfPairs:
        links_dic[x].append(y)
    vertexes_list = list(vertexes)

    result = {}
    # teleports = False -> follow the link.
    if teleports is False:
        result = teleport_off(links_dic, page_ranks, vertexes_list, numIters)
    else:
        flags = ['on', 'off']
        result = teleport_on(links_dic, page_ranks, vertexes_list, numIters, flags)
    for val in result:
        result[val] = result[val] / divider
    return result




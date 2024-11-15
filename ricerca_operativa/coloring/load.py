#!/bin/python3


def load(file):
    txt = open(file, 'r').read()
    graph = {}
    for line in txt.splitlines():
        nodes = line.split()
        start = int(nodes[0])
        end = int(nodes[1])
        if start not in graph:
            graph[start] = set()
        graph[start].add(end)
        if end not in graph:
            graph[end] = set()
        graph[end].add(start)
    return graph


def def_load():
    return load('graph.txt')

from collections import defaultdict


class Graph:

    def __init__(self):
        self.__edges = defaultdict(list)

    @property
    def edges(self):
        return self.__edges

    def addEdge(self, u, v):
        self.__edges[u].append(v)
        self.__edges[v].append(u)

    def remEdge(self, u, v):
        self.__edges[u].remove(v)
        self.__edges[v].remove(u)

    def isEulerian(self) -> bool:
        count = 0

        for l in self.__edges.values():
            if len(l) % 2 != 0:
                count += 1

        if count == 0 or count == 2:
            return True

        return False

    def reachCount(self, u, visited) -> int:
        count = 1
        visited[u] = True
        for i in self.__edges[u]:
            if not visited[i]:
                count += self.reachCount(i, visited)

        return count

    def isValidNext(self, u, v) -> bool:
        if len(self.__edges[u]) == 1:
            return True
        else:
            visited = [False] * len(self.__edges.keys())  # init list with False values
            count1 = self.reachCount(u, visited)

            self.remEdge(u, v)
            visited = [False] * len(self.__edges.keys())  # init list with False values
            count2 = self.reachCount(u, visited)
            self.addEdge(u, v)

            return count1 <= count2

    def computeFleury(self) -> list:
        result = list()

        r = -1
        for k, v in self.__edges.items():
            if len(v) % 2 != 0:
                r = k
                break

        if r == -1:
            r = next(iter(self.__edges.keys()))  # get the first key from the dictionary

        def rec_find(u):
            for v in self.__edges[u]:
                if self.isValidNext(u, v):
                    self.remEdge(u, v)
                    result.append((u, v))
                    rec_find(v)
                    break

        rec_find(r)

        return result


graph = Graph()

graph.addEdge(1, 0)
graph.addEdge(0, 2)
graph.addEdge(2, 1)
graph.addEdge(0, 3)
graph.addEdge(3, 4)
graph.addEdge(3, 2)
graph.addEdge(3, 1)
graph.addEdge(2, 4)

if graph.isEulerian():
    print(', '.join([str(item[0]) + '-' + str(item[1]) for item in graph.computeFleury()]))
else:
    print("This isn't valid graph for Fleury's algorithm (it must be Eulerian graph)!")

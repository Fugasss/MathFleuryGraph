import copy
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

        for l in self.__edges.keys():
            connected = self.__edges[l]

            if len(connected) == 1 and connected[0] == l:
                return False

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
            visited = dict.fromkeys(self.__edges.keys(), False)
            count1 = self.reachCount(u, visited)

            self.remEdge(u, v)
            visited = dict.fromkeys(self.__edges.keys(), False)
            count2 = self.reachCount(u, visited)
            self.addEdge(u, v)

            return count1 <= count2

    def computeFleury(self) -> list:
        result = list()

        edges_backup = copy.deepcopy(self.__edges)

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

        self.__edges = edges_backup

        return result


graph = Graph()

# example input:
# 8
# 1 0
# 0 2
# 2 1
# 0 3
# 3 4
# 3 2
# 3 1
# 2 4


count: int
while True:
    inp = input("Enter edges count: ")

    if not inp.isdigit():
        print("You must enter a number")
        continue

    count = int(inp)
    break

print("\tEnter edges in following formats: a-b, a b, 1-2, or 1 2")
print("Enter edges line by line!")

i = 0
while i != count:
    e = input()

    sep = ' '
    if e.find(' ') != -1:
        sep = ' '
    elif e.find('-') != -1:
        sep = '-'
    else:
        print("Wrong format! Try again.")
        continue

    nums = e.split(sep)

    if len(nums) > 2:
        print("Wrong format! Try again.")
        continue

    graph.addEdge(nums[0], nums[1])

    i += 1

if graph.isEulerian():
    path = graph.computeFleury()
    print('\tPath in 2 formats:')
    print(', '.join([str(item[0]) + '-' + str(item[1]) for item in path]), 'or')
    print(path[0][0],
          '->',
          ' -> '.join([str(item[0]) for item in path[1:-1]]),
          '->',
          path[-1][0],
          '->',
          path[-1][1])
else:
    print("This isn't valid graph for Fleury's algorithm (it must be Eulerian graph)!")

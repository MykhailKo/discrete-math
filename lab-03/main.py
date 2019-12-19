from itertools import islice


def do_bfs(edges, tops):
    start = int(input("Введіть вершину початок: "))
    if start not in range(1, tops+1):
        print("У графі не існує заданої вершини")
        exit()
    queue = [start]
    tops = [t for t in range(1, tops+1) if t != start]
    num = 1
    for e in edges: e.sort()
    edges.sort()
    print("  v  |BFS-n|  queue content")
    print("---------------------------")
    print("%3d  |%3d  |" % (start, num) + "  " + str(queue).strip('[]'))
    while queue:
        start = queue[0]
        for p in edges:
            if start in p and p[0 if p.index(start) else 1] in tops:
                i = 0 if p.index(start) else 1
                queue.append(p[i])
                tops.remove(p[i])
                num += 1
                print("%3d  |%3d  |" % (p[i], num) + "  " + str(queue).strip('[]'))
        del queue[0]
        print("  -  |  -  |  " + str(queue).strip('[]'))


def do_dfs(edges, tops):
    start = int(input("Введіть вершинк початок: "))
    if start not in range(1, tops+1):
        print("У графі не існує заданої вершини")
        exit()
    stack = [start]
    tops = [t for t in range(1, tops+1) if t != start]
    num = 1
    for e in edges: e.sort()
    edges.sort()
    print("  v  |DFS-n|  stack content")
    print("---------------------------")
    print("%3d  |%3d  |" % (start, num) + "  " + str(stack).strip('[]'))
    while stack:
        start = stack[len(stack)-1]
        cur_v = [e[0] if e.index(start) else e[1] for e in edges if start in e and e[0 if e.index(start) else 1] in tops]
        while cur_v:
            cur_v = [e[0] if e.index(start) else e[1] for e in edges if start in e and e[0 if e.index(start) else 1] in tops]
            if cur_v and cur_v[0] in tops:
                stack.append(cur_v[0])
                tops.remove(cur_v[0])
                num += 1
                start = cur_v[0]
                print("%3d  |%3d  |" % (cur_v[0], num) + "  " + str(stack).strip('[]'))
        del stack[len(stack) - 1]
        print("  -  |  -  |  " + str(stack).strip('[]'))


file = open('condition.txt')
tops_num = int(file.read(1))
edges_num = int(file.read(3))
edge_list = []
for edge in islice(file, 0, edges_num):
    ep = []
    for top in edge.split(' ', 1):
        ep.append(int(top))
    edge_list.append(ep)
if edges_num != len(edge_list):
    print("\nКількість ребер не співпадає у із заданим списком, перевірте файл condition.txt")
    exit()
print("Кількість вершин: " + str(tops_num))
print("Кількість ребер: " + str(edges_num))
print("Список граней: ", edge_list)

print(
    "\nНатисніть 1 щоб обійти граф вшир BFS"
    "\nНатисніть 2 щоб обійти граф вглиб DFS"
    "\nPress f щоб завешити роботу"
)
control = ""
while control != "f":
    control = input('\n')
    if control == '1': do_bfs(edge_list, tops_num)
    if control == '2': do_dfs(edge_list, tops_num)

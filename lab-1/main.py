from itertools import islice


def print_matrix(mat):
    for r in mat:
        for el in r:
            print("%2d" % el, end=' ')
        print()


def gen_adj_mat(tops, e_list):
    adj_mat = [0] * tops
    for i in range(tops):
        adj_mat[i] = [0] * tops
    for e in e_list:
        adj_mat[e[0]-1][e[1]-1] = 1
    print("\nМатриця суміжності: \n")
    print_matrix(adj_mat)
    return adj_mat


def gen_inc_mat(tops, edges, e_list):
    inc_mat = [0] * tops
    for i in range(tops):
        inc_mat[i] = [0] * edges
    for t in range(len(inc_mat)):
        for e in range(len(inc_mat[t])):
            if e_list[e][0] == e_list[e][1] == t + 1:
                inc_mat[t][e] = 2
            elif e_list[e][0] == t + 1:
                inc_mat[t][e] = -1
            elif e_list[e][1] == t + 1:
                inc_mat[t][e] = 1
    print("\nМатриця інцедентності: \n")
    print_matrix(inc_mat)
    return inc_mat


def get_tops_deg(tops, mat, prt):
    mono = 0
    l_deg = 0
    degrees = []
    for t in range(tops):
        deg = 0
        for e in mat:
            if t + 1 in e: deg += 1
        if prt:
            print("\nСтепінь вершини " + str(t + 1) + ": " + str(deg), end='')
        mono += deg
        if deg != 0: l_deg = deg
        degrees.append(deg)
    if prt:
        if degrees.count(l_deg) == tops: print("\nГраф є однорідним, його степінь " + str(l_deg))
        else: print("\n Граф не є однорідним")
    return degrees


def check_tops(degs):
    print("\nКінцеві вершини: ", end='')
    for t in range(len(degs)):
        if degs[t] == 1: print(str(t + 1), end=', ')
    print("\nІзольовані вершини: ", end='')
    for t in range(len(degs)):
        if degs[t] == 0: print(str(t + 1), end=', ')
    print()


file = open('condition.txt')
tops_num = int(file.read(1))
edges_num = int(file.read(3))
edge_list = []
for edge in islice(file, 0, edges_num):
    ep = []
    for top in edge.split(' ', 1):
        ep.append(int(top))
    edge_list.append(ep)
print("Кількість вершин: " + str(tops_num))
print("Кількість ребер: " + str(edges_num))
print("Список граней: ", edge_list)
print("\nНатисніть 1 щоб вивести матрицю суміжності"
          "\nНатисніть 2 щоб вивести матрицю інцедентності"
          "\nНатисніть 3 щоб вивести степені вершин"
          "\nНатисніть 4 щоб вивести ізольовані та кінцеві вершини"
          "\nPress f щоб завешити роботу")
control = ''
degrees = []
while control != 'f':
    control = input("\n")
    if control == '1': gen_adj_mat(tops_num, edge_list)
    elif control == '2': gen_inc_mat(tops_num, edges_num, edge_list)
    elif control == '3': degrees = get_tops_deg(tops_num, edge_list, True)
    elif control == '4':
        degrees = get_tops_deg(tops_num, edge_list, False)
        check_tops(degrees)


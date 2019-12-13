from itertools import islice
import numpy as np


def print_matrix(mat):
    for r in mat:
        for el in r:
            print("%2s" % el, end=' ')
        print()


def gen_dist_matrix(mat, degree, prt):
    dist_mat = mat
    res_mat = [[0]*len(mat) for i in range(len(mat))]
    temp_mat = mat
    done = 1
    while done < degree:
        for r in range(len(res_mat)):
            for d in range(len(res_mat[r])):
                for i in range(len(mat)): res_mat[r][d] += temp_mat[r][i]*mat[i][d]
        temp_mat = res_mat
        for r in range(len(res_mat)):
            for d in range(len(res_mat[r])):
                if res_mat[r][d] != 0 and r != d and dist_mat[r][d] == 0: dist_mat[r][d] = done + 1
        res_mat = [[0]*len(mat) for i in range(len(mat))]
        done += 1
    p_dist_mat = [['oo' if dist_mat[d][t] == 0 and t != d else dist_mat[d][t] for t in range(len(dist_mat[d]))] for d in range(len(dist_mat))]
    if prt:
        print("Матриця відстаней: \n")
        print_matrix(p_dist_mat)
    return dist_mat


def gen_reach_mat(mat, prt):
    reach_mat = [[1 if mat[i][j] != 0 or j == i else 0 for j in range(len(mat[i]))] for i in range(len(mat))]
    if prt:
        print("Матриця досяжності: \n")
        print_matrix(reach_mat)
    return reach_mat


def find_center_radius(mat):
    cent = []
    tops_exc = []
    for t in range(len(mat)):
        tops_exc.append(max(mat[t]))
    rad = min(tops_exc)
    if tops_exc.count(rad) > 1:
        start = tops_exc.index(rad)
        for i in range(tops_exc.count(rad)):
            c = tops_exc.index(rad, start)
            cent.append(c+1)
            start = tops_exc.index(rad, c) + 1
    return rad, cent


def find_diameter(mat):
    diam = 0
    for t in mat:
      if diam < max(t): diam = max(t)
    return diam


def get_stages(mat):
    t = int(input('\nВідносно якої вершини визначати яруси?\n'))
    print("Яруси вершшини " + str(t) + ":")
    ds = mat[t-1]
    stages = [[ds.index(ds[d], d)+1 for d in range(len(ds)) if ds[d] == st] for st in range(1, max(ds)+1)]
    for i in range(len(stages)):
        print("Ярус" + str(i+1) + ":", end=" ")
        for j in stages[i]: print(str(j) + ",", end=" ")
        print()


def get_connect_type(mat, reach_mat_no):
    type = 0
    con_tops = 0
    for t in reach_mat_no:
        if t.count(1) == len(reach_mat_no): con_tops += 1
    if con_tops == len(reach_mat_no): type = 1
    r = np.array(mat)
    tr = r.transpose()
    single_con = r + tr
    single_con = single_con.tolist()
    ch1 = [1 for r in single_con if r.count(0) == 0]
    if len(ch1) == len(single_con): type = 2
    ch2 = [1 for r in mat if r.count(1) == len(r)]
    if len(ch2) == len(mat): type = 3
    print("Тип зв'язності графа: ", end='')
    if type == 1: print("слабко зв'язаний")
    elif type == 2: print("однобічно зв'язаний")
    elif type == 3: print("сильно зв'язаний")
    else: print("незв'язний")


def gen_adj_mat(tops, e_list, org):
    adj_mat = [[0]*tops for i in range(tops)]
    for e in e_list:
        adj_mat[e[0]-1][e[1]-1] = 1
        if not org: adj_mat[e[1]-1][e[0]-1] = 1
    return adj_mat


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
print("!!!Дана програма використовує python модуль numpy, "
          "\nякщо він не встановлений на вашому комп'ютері виконайте команду"
          "\npip install numpy!!!\n")
print("Кількість вершин: " + str(tops_num))
print("Кількість ребер: " + str(edges_num))
print("Список граней: ", edge_list)

print("\nЯкий граф задано у файлі?"
          "\nНатисніть 1 для неорієнтованого"
          "\nНатисніть 2 для орієнтованого"
          "\nPress f щоб завешити роботу")
graph_type = input('\n')
if graph_type == '1':
    adj_matrix = gen_adj_mat(tops_num, edge_list, False)
    dist_matrix = gen_dist_matrix(adj_matrix, tops_num, False)
    print("\nНатисніть 1 щоб вивести матрицю відстаней"
          "\nНатисніть 2 щоб вивести матрицю досяжності"
          "\nНатисніть 3 щоб вивести метричні характеристики"
          "\nНатисніть 4 щоб вивести яруси"
          "\nPress f щоб завешити роботу")
    control = ''
    while control != 'f':
        control = input('\n')
        if control == '1': dist_matrix = gen_dist_matrix(adj_matrix, tops_num, True)
        elif control == '2': reach_matrix = gen_reach_mat(dist_matrix, True)
        elif control == '3':
            diameter = find_diameter(dist_matrix)
            print("Діаметр: " + str(diameter) + "\n")
            radius, centers = find_center_radius(dist_matrix)
            print("Радіус: " + str(radius) + "\n")
            print("Центральні вершини: " + str(centers) + "\n")
        elif control == '4': get_stages(dist_matrix)
elif graph_type == '2':
    reach_mat_no = gen_reach_mat(gen_dist_matrix(gen_adj_mat(tops_num, edge_list, False), tops_num, False), False)
    adj_matrix = gen_adj_mat(tops_num, edge_list, True)
    dist_matrix = gen_dist_matrix(adj_matrix, tops_num, False)
    reach_matrix = gen_reach_mat(dist_matrix, False)
    print("\nНатисніть 1 щоб вивести матрицю відстаней"
          "\nНатисніть 2 щоб вивести матрицю досяжності"
          "\nНатисніть 3 щоб вивести тип зв'язності"
          "\nPress f щоб завешити роботу")
    control = ''
    while control != 'f':
        control = input('\n')
        if control == '1': dist_matrix = gen_dist_matrix(adj_matrix, tops_num, True)
        elif control == '2': reach_matrix = gen_reach_mat(dist_matrix, True)
        elif control == '3': get_connect_type(reach_matrix, reach_mat_no)
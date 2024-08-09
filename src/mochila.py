# -*- coding: utf-8 -*-
import gurobipy as gp
from gurobipy import GRB

#Leitura de Arquivo
with open('entrada.txt', 'r') as f:
    linha = f.readline().strip()
    n,m = map(int,linha.split())
    linha = f.readline().strip()
    b = list(map(float, linha.split()))
    p = [None for i in range(n)]
    w = [None for i in range(n)]
    for i in range(n):
        linha = f.readline().strip().split(' ')
        p[i] = float(linha[0])
        w[i] = float(linha[1])

# Cria um novo modelo
model = gp.Model()
model.setParam(GRB.Param.LogToConsole, 1)
# Cria as variáveis do problema
x = [model.addVar(lb=0, ub=1, vtype=GRB.BINARY) for i in range(n) for j in range (m)]
len(x)

# Define a função objetivo
obj = gp.LinExpr()
for i in range(n):
    for j in range(m):
        obj = obj + p[i] * x[j + i*m]
model.setObjective(obj, sense=GRB.MAXIMIZE)

# Define as restrições de capacidade de cada mochila
for j in range(m):
    exprm = gp.LinExpr()
    for i in range(n):
        exprm = exprm + w[i] * x[j + i*m]
    model.addConstr(exprm <= b[j])
    
# Define as restrições de limite máximo 1 dos itens
for i in range(n):
    exprn = gp.LinExpr()
    for j in range(m):
        exprn = exprn + x[j + i*m]
    model.addConstr(exprn <= 1)

# Resolve o problema!
model.optimize()
# Dados da solução encontrada
print('---------------------------------------------------')
print(f'Solução Ótima')
print('---------------------------------------------------')
print(f'Valor da Função Objetivo: {round(model.objVal, 1)}')
for j in range(m):
    count = 0
    print(f'Itens da Mochila {j}: [', end='')
    for i in range(n):
        if x[j+i*m].X:
            if count == 0:
                print(f'{i}', end='')
                count += 1
            else:
                print(f', {i}', end='')
    print(']')

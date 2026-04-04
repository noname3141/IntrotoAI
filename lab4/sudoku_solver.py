import pycosat as psat
import sys, os, copy
input_file = sys.argv[1]

with open(input_file, 'r') as file:
    content = file.read()
    data = content.split("\n")

data.pop()

games = []

for i in data:
    row = 0
    col = 0
    n = 9
    m = 9

    mat = [[0 for _ in range(m)] for _ in range(n)]
    for j in i:
        if row == 9:
            col += 1
        row %= 9
        mat[row][col] = j
        row += 1
    
    games.append(mat)

def cell(x, y, z):
    return 100*x + 10*y + z + 1

def decell(x):
    return x//100

solution = []
base_clause = []
atleast_one = []
atmax_one = []
uniqrow = []
uniqcol = []
smaller_block = []
    
for rw in range(0, 9):
    for cl in range(0, 9):
        l = []
        for n1 in range(0, 9):
            l.append(cell(n1, rw, cl))
        atleast_one.append(l)
    
for rw in range(0, 9):
    for cl in range(0, 9):
        for n1 in range(0, 9):
            for m1 in range(n1+1, 9):
                x1 = [-1*cell(n1, rw, cl), -1*cell(m1, rw, cl)]
                atmax_one.append(x1)

for rw in range(0, 9):
    for n1 in range(0, 9):
        l = []
        for cl in range(0, 9):
            l.append(cell(n1, rw, cl))
        uniqrow.append(l)

for cl in range(0, 9):
    for n1 in range(0, 9):
        l = []
        for rw in range(0, 9):
            l.append(cell(n1, rw, cl))
        uniqcol.append(l)
    
for n1 in range(0, 3):
    for m1 in range(0, 3):
        for num in range(0, 9):
            l = []
            for j in range(n1*3, n1*3 + 3):
                for k in range(m1*3, m1*3 + 3):
                    l.append(cell(num, j, k))
            smaller_block.append(l)

for group in atleast_one:
    base_clause.append(group)

for group in atmax_one:
    base_clause.append(group)

for group in uniqrow:
    base_clause.append(group)

for group in uniqcol:
    base_clause.append(group)

for group in smaller_block:
    base_clause.append(group)

for group in smaller_block:
    for n1 in range(len(group)):
        for m1 in range(n1 + 1, len(group)):
            base_clause.append([-group[n1], -group[m1]])

for i in games:
    #main loop in which each clause will be made.
    clauses = copy.deepcopy(base_clause)
    
    init = []

    for n1 in range(0, 9):
        for m1 in range(0, 9):
            if i[n1][m1] != '.':
                i1 = int(i[n1][m1]) - 1
                init.append([cell(i1, n1, m1)])
                
    clauses.extend(init)
    
    sl = psat.solve(clauses)
    
    out = []

    for i in sl:
        if i > 0:
            out.append(i)
    
    for n1 in range(0, len(out)):
        for m1 in range(    n1 + 1, len(out)):
            if(out[n1] % 100 > out[m1] % 100):
                out[n1], out[m1] = out[m1], out[n1]
   
    final = []

    for i in out:
        final.append(decell(i))

    solution.append(final)


output_file = os.path.join(os.path.dirname(os.path.abspath(input_file)), "output.txt")

result = ''

for i in solution:
    for j in i:
        result += str(j)
    result += '\n'

print(result)

try:
    with open(output_file, "w") as f:
        f.write(result)
except:
    print(result)

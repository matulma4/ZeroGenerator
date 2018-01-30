import random
import operator
import math


class Config():
    def __init__(self, filename):
        self.args = {}
        with open(filename) as f:
            for line in f:
                if line[0] != "#" and len(line) > 1:
                    l = line.strip().split('=')
                    self.args[l[0]] = eval(l[1])

    def __getitem__(self, item):
        return self.args[item]


class Piece():
    def __init__(self, op, val, diag, long):
        self.val = val
        self.op = op
        self.diag = diag
        self.long = long


class Element():
    def __init__(self,i, j, x, y):
        self.empty = False
        self.value = 0
        self.dirs = range(1, 10)
        self.neighbors = []
        if i > 0:
            if j > 0:
                self.neighbors.append([i-1,j-1])
            if j < y-1:
                self.neighbors.append([i-1,j+1])
            self.neighbors.append([i-1, 0])
        elif i < x-1:
            if j > 0:
                self.neighbors.append([i+1,j-1])
            if j < y-1:
                self.neighbors.append([i+1,j+1])
            self.neighbors.append([i+1, 0])
        else:
            if j > 0:
                self.neighbors.append([0,j-1])
            if j < y-1:
                self.neighbors.append([0,j+1])


def is_perfect( value, exponent ):
    root = value ** ( 1.0 / exponent )
    root = long( round( root ) )
    return root ** exponent  == value

def check_neighbors(b, i, j, config):
    counter = 0
    s = [0]
    t = [0]
    if i > 0:
        s.append(-1)
    if i < len(b)-1:
        s.append(1)
    if j > 0:
        t.append(-1)
    if j < len(b[0])-1:
        t.append(1)
    for u in s:
        for v in t:
            if config["diag"]:
                if (not math.isnan(b[i+u][j+v])) and (u != 0 or v != 0):
                    counter += 1
            else:
                if (not math.isnan(b[i+u][j+v])) and bool(u) != bool(v):
                    counter += 1
    return counter


def generate_board(config):
    x = random.randint(2, config["x"])
    y = random.randint(2, config["y"])
    b = [[0 for _ in range(y)] for _ in range(x)]
    c = [[0 for _ in range(y)] for _ in range(x)]
    u = 0
    while u < config["out"]:
        # TODO fix infinite loop
        i = random.randint(0,x-1)
        j = random.randint(0,y-1)
        if check_neighbors(b, i, j, config) > 0:
            b[i][j] = float("nan")
            u += 1
    for i in range(len(b)):
        for j in range(len(b[0])):
            c[i][j] = check_neighbors(b, i, j, config)

    return b, c


def get_operators(c):
    result = []
    if c["add"]:
        result += ["+", "-"]
    if c["mult"]:
        result += ["*", "/"]
    if c["pow"]:
        result += ["pow", "root"]
    if c["mod"]:
        result += ["%"]
    return result


def modify_board(b, i, j, op, val):
    rt = lambda x,y: x**(float(1)/float(y))
    # TODO change range
    m = lambda x,y: random.randint(0,5)*y + x
    # sic!
    ops = {'+': operator.sub,'-': operator.add, '*': operator.div,'/': operator.mul,'%': m, 'pow': rt, 'root': operator.pow}
    return ops[op](b[i][j], val)



def generate_operators(b, c, config):
    ops = get_operators(config)
    result = []
    diff = 3 if config["long"] else 2
    dirs = [[0,1], [0,-1],[1,0],[-1,0]]
    dirs_diag = dirs + [[1,1], [1,-1],[1,-1],[-1,-1]]
    while True:
        if config["diag"]:
            pass
        else:
            i = random.randint(0,len(b)-1)
            j = random.randint(0,len(b[0])-1)
            if b[i][j] < 0:
                continue
            dir = dirs[random.randint(0,len(dirs)-1)]
            dir_x = dir[0]
            dir_y = dir[1]
            d = random.randint(2, diff)
            viable = True
            for k in range(0, d):
                try:
                    # if b[i + k*dir_x][j + k*dir_y] < 0:
                    if math.isnan(b[i + k*dir_x][j + k*dir_y]):
                        viable = False
                        break
                except IndexError:
                    viable = False
                    break
            if not viable:
                continue
            op = ops[random.randint(0, len(ops)-1)]
            v = random.randint(0,config["max_"+op])
            for k in range(0, d):
                b[i + k * dir_x][j + k * dir_y] = modify_board(b, i + k * dir_x, j + k * dir_y, op, v)
                c[i + k * dir_x][j + k * dir_y] -= 1

            result.append(Piece(op, v, config["diag"], config["long"]))


    return result


if __name__ == '__main__':
    random.seed(43)
    conf = Config("config.dat")
    board, counter = generate_board(conf)
    pieces = generate_operators(board, counter, conf)
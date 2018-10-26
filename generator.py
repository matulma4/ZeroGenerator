import datetime
import math
import operator
import random


class Config:
    def __init__(self, filename):
        self.args = {}
        with open(filename) as f:
            for line in f:
                if line[0] != "#" and len(line) > 1:
                    l = line.strip().split('=')
                    self.args[l[0]] = eval(l[1])

    def __getitem__(self, item):
        return self.args[item]


class Piece:
    def __init__(self, op, val, vert, diag, long_piece):
        self.val = val
        self.op = op
        self.diag = diag
        self.long_piece = long_piece
        self.vert = vert

    def __repr__(self):
        a = "horizontal "
        if self.vert:
            a = "vertical "
        return a + self.op + " " + str(self.val)


class Element():
    def __init__(self, i, j, x, y, diag):
        self.empty = False
        self.used = False
        self.value = 0
        self.dirs = range(1, 10)
        self.neighbors = []
        self.i = i
        self.j = j
        if i > 0:
            if j > 0 and diag:
                self.neighbors.append([i - 1, j - 1])
            if j < y - 1 and diag:
                self.neighbors.append([i - 1, j + 1])
            self.neighbors.append([i - 1, j])
        if i < x - 1:
            if j > 0 and diag:
                self.neighbors.append([i + 1, j - 1])
            if j < y - 1 and diag:
                self.neighbors.append([i + 1, j + 1])
            self.neighbors.append([i + 1, j])
        if j > 0:
            self.neighbors.append([i, j - 1])
        if j < y - 1:
            self.neighbors.append([i, j + 1])

    def check_neighbors(self, b):
        for n in self.neighbors:
            if len(b[n[0]][n[1]].neighbors) <= 1:
                return False
        return True

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


def is_perfect(value, exponent):
    root = value ** (1.0 / exponent)
    root = long(round(root))
    return root ** exponent == value


def check_neighbors(b, i, j, config):
    counter = 0
    s = [0]
    t = [0]
    if i > 0:
        s.append(-1)
    if i < len(b) - 1:
        s.append(1)
    if j > 0:
        t.append(-1)
    if j < len(b[0]) - 1:
        t.append(1)
    for u in s:
        for v in t:
            if config["diag"]:
                if (not math.isnan(b[i + u][j + v])) and (u != 0 or v != 0):
                    counter += 1
            else:
                if (not math.isnan(b[i + u][j + v])) and bool(u) != bool(v):
                    counter += 1
    return counter


def generate_board(config):
    x = random.randint(2, config["x"])
    y = random.randint(2, config["y"])
    b = [[Element(i, j, x, y, config["diag"]) for j in range(y)] for i in range(x)]
    u = 0
    while u < config["out"]:
        # TODO fix infinite loop
        i = random.randint(0, x - 1)
        j = random.randint(0, y - 1)
        if b[i][j].check_neighbors(b):
            b[i][j].empty = True
            for s, t in b[i][j].neighbors:
                b[s][t].neighbors.remove([i, j])
            u += 1

    return b


def check_operation(val1, val2, mod_val, op):
    if op == "*":
        return val1 % mod_val == 0 and val2 % mod_val == 0 and (val1 != 0 or val2 != 0)
    elif op == "/":
        return val1 != 0 and val2 != 0
    elif op == "pow":
        return is_perfect(val1, mod_val) and is_perfect(val2, mod_val)
    else:
        return True


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


def check_viable(b, d, i, j, s, t):
    dir_x = s - i
    dir_y = t - j
    for k in range(0, d):
        try:
            if b[i + k * dir_x][j + k * dir_y].empty:
                return False
        except IndexError:
            return False
    return True


def modify_board(element, op, val):
    rt = lambda x, y: x ** (float(1) / float(y))
    # TODO change range
    m = lambda x, y: random.randint(0, 5) * y + x
    # sic!
    ops = {'+': operator.sub, '-': operator.add, '*': operator.div, '/': operator.mul, '%': m, 'pow': rt,
           'root': operator.pow}
    return ops[op](element.value, val)


def generate_pieces(b, config):
    ops = get_operators(config)
    result = []
    diff = 3 if config["long"] else 2
    covered = len(b) * len(b[0]) - config["out"]
    while covered > 0:
        if True:
            i = random.randint(0, len(b) - 1)
            j = random.randint(0, len(b[0]) - 1)
            if b[i][j].empty or b[i][j].used:
                continue
            if len(b[i][j].neighbors) == 0:
                covered -= 1
                b[i][j].used = True
                continue
            d = random.randint(2, diff)
            neighbor = b[i][j].neighbors[random.randint(0, len(b[i][j].neighbors) - 1)]
            if not check_viable(b, d, i, j, neighbor[0], neighbor[1]):
                continue
            op = ops[random.randint(0, len(ops) - 1)]
            min_val = 1
            if op == "*" or op == "/":
                min_val = 2
            v = random.randint(min_val, config["max_" + op])
            elements = [[i, j], neighbor]
            if check_operation(b[i][j].value, b[neighbor[0]][neighbor[1]].value, v, op):
                vert = False if neighbor[0] == i else True
                diag = False
                long_piece = False if diff == 2 else True
                if neighbor[0] != i and neighbor[1] != j:
                    diag = True
                for e in range(len(elements)):
                    el = elements[e]
                    element = b[el[0]][el[1]]
                    element.neighbors.remove(elements[e - 1])
                    element.value = modify_board(element, op, v)
                    # r = random.randint(0, 4)
                    # if r > 2:
                    #     covered -= 1
                    #     b[el[0]][el[1]].used = True
                result.append(Piece(op, v, vert, diag, long_piece))
    return result


def write_result(fname, result, b):
    with open(fname, "w") as g:
        for e in range(len(b)):
            for f in range(len(b[0])):
                el = b[e][f]
                g.write(",".join([str(el.i), str(el.j), str(el.value), str(el.empty)]) + "\n")

        for piece in result:
            g.write(",".join(
                [str(piece.op), str(piece.val), str(piece.vert), str(piece.diag), str(piece.long_piece)]) + "\n")


if __name__ == '__main__':
    random.seed(datetime.datetime.now())
    conf = Config("config.dat")
    board = generate_board(conf)
    pieces = generate_pieces(board, conf)
    write_result("test.csv", pieces, board)

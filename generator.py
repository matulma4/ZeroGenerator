import random


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


def check_neighbors(b, i, j):
    counter = 0
    s = []
    t = []
    if i >= 0:
        s.append(-1)
    if i < len(b)-1:
        s.append(1)
    if j >= 0:
        t.append(-1)
    if j < len(b[0])-1:
        t.append(1)
    for u in s:
        for v in t:
            if b[i+u][j+v] >= 0:
                counter += 1
    return counter > 1


def generate_board(config):
    x = random.randint(2, config["x"])
    y = random.randint(2, config["y"])
    b = [[0 for _ in range(y)] for _ in range(x)]
    c = [[0 for _ in range(y)] for _ in range(x)]
    u = 0
    while u < config["out"]:
        i = random.randint(0,x-1)
        j = random.randint(0,y-1)
        if check_neighbors(b, i, j):
            b[i][j] = -1
            u += 1
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


def generate_operators(b, c, config):
    pass

if __name__ == '__main__':
    random.seed(43)
    conf = Config("config.dat")
    board, counter = generate_board(conf)
    pass
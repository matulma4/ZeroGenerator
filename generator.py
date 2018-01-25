
class Config():
    def __init__(self, filename):
        self.args = {}
        with open(filename) as f:
            for line in f:
                if line[0] != "#" and len(line) > 1:
                    l = line.strip().split('=')
                    self.args[l[0]] = eval(l[1])


if __name__ == '__main__':
    c = Config("config.dat")
    pass
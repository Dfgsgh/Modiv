import argparse

parser = argparse.ArgumentParser(description="Modiv interpreter")
parser.add_argument("-f", "--file", type=str, required=True, help="Specify the code file")
args = parser.parse_args()

with open(args.file, "r") as f:
    code = f.read()

labels = {}
acc = int(1)
linenum = 0


def nmod(n):
    global acc
    a = acc
    r = 0
    while a % n == 0:
        a = a//n
        r += 1
    return r

def evaluate(expression):
    global acc
    while 'din' in expression:
        expression = expression.replace('din', str(int(input())), 1)

    while 'ain' in expression:
        expression = expression.replace('ain', str(ord(input()[0])), 1)

    expression = expression.replace('acc', str(acc))
    expression = expression.replace('^', '**')
    expression = expression.replace('/', '//')

    allowed = set("0123456789+-*/() nmod\n")

    if set(expression.lower()).issubset(allowed):
        x = eval(expression, {"nmod": nmod})
        if isinstance(x, int) and x >= 0:
            return x
        else:
            raise ValueError("Negative or non-integer result not allowed.")
    else:
        raise ValueError("Unsafe characters in expression.")



    
def label(name, number):
    global labels
    labels[name.strip()] = number

def SET(x):
    global acc
    acc = x

def Jump(name):
    global linenum, labels
    linenum = labels[name]

def CJump(name, x):
    global acc, linenum, labels
    if x != 0:
        Jump(name)

def AOut(x):
    print(chr(x), end='')

def DOut(x):
    print(x, end='')

def labeling():
    global labels, code
    y = 0
    for line in code.split('\n'):
        if line.startswith(':'):
            label(line.strip(": "),y)
            y+=1

def run(line):
    global acc, labels, linenum
    if line.startswith('SET'):
        SET(evaluate(line.strip('SET')))
    elif line.startswith('JUMP'):
        Jump(line.strip('JUMP '))
    elif line.startswith('CJUMP'):
        line = line.strip('CJUMP ')
        smth = line.split(' ', 1)
        CJump(smth[0],evaluate(smth[1]))
    elif line.startswith('AOUT'):
        AOut(evaluate(line.strip('AOUT')))
    elif line.startswith('DOUT'):
        DOut(evaluate(line.strip('DOUT')))
    else:
        pass


def execute():
    global code, linenum
    labeling()
    code = code.split('\n')
    while linenum < len(code):
        run(code[linenum])
        linenum += 1

execute()

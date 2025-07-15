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
    # Replace din inputs
    while 'din' in expression:
        expression = expression.replace('din', str(int(input())), 1)

    # Replace ain inputs
    while 'ain' in expression:
        expression = expression.replace('ain', str(ord(input()[0])), 1)

    # Replace '^' with '**'
    expression = expression.replace('^', '**')

    allowed = set("0123456789abcdefghijklmnopqrstuvwxyz+-*/(), ")
    if set(expression.lower()).issubset(allowed):
        # Provide nmod and rely on global acc for 'acc'
        x = eval(expression, {"nmod": nmod})
        if isinstance(x, int) and x >= 0:
            return x
        else:
            raise ValueError("Negative or non-integer result not allowed.")
    else:
        raise ValueError("Unsafe characters in expression.")


    
def label(name, number):
    global labels
    labels[name] = number

def SET(x):
    global acc
    acc = x

def Jump(name):
    global linenum, labels
    linenum = labels[name]

def CJump(name, x):
    global acc, linenum, labels
    if acc % x == 0:
        SET(acc // x)
        Jump(name)

def AOut(x):
    print(chr(x), end='')

def DOut(x):
    print(x, end='')

def runline(line):
    global linenum
    if line.startswith(':'):
        label(line.strip(':'), linenum)
    elif line.startswith('SET'):
        SET(evaluate(line[2:]))
    
ignore = ['#', ';']
newChars = ['(', ')', '{', '}', ',', '#']
vars = []
funcs = []
terms = ['bid', 'exalt', 'hark', 'be', 'eternal', 'doth', 'with', 'without']
declares = ['bid', 'eternal', 'doth']
newDec = 0
def error(line=None, wholeLine=None, type=None, term=None):
    if type == 'declaration':
        pass
    elif type == 'unexpected':
        print(f'And it came to pass that the term, even {term}, was found in the midst of the code—known to the learned, yet out of season and without cause.')
    elif type == 'badComma':
        print(f'At line {line}, a comma did appear, yet it belonged not; for another parameter was looked for, and the comma was found wanting.')
    elif line:
        print(f'Lo, at line {line}, there arose an error, sudden and without warning.')
    
    if wholeLine:
        print(' '.join(wholeLine))
    else:
        print('We have searched the lines and beheld them with care, but the source remaineth in darkness.')
    if term:
        print(term)
    print('vars')
    for var in vars:
        print(var.type, var.name, '=', var.value)
    print('funcs')
    for func in funcs:
        print(func.name, func.params, func.script)
    exit(1)

def declare(term, line):
    global declaring
    global newDec
    if term in declares:
        if declaring:
            error(line, None, 'unexpected', term)
        else:
            declaring = True
            if term == 'doth':
                newDec = Function(line)
            else:
                newDec = Variable(line, term)

class Variable():
    def __init__(self, line=0, type=0, name=0, value=None):
        self.line = line
        self.type = type
        self.name = name
        
class Function():
    def __init__(self, line=0, name=0, params=[], script=0):
        self.type = 'function'
        self.line = line
        self.name = name
        self.params = params
        self.script = script
        
    def runScript(self):
        pass

declaring = False
onLine = 0

def run(code):
    assigning = False
    addParams = False
    nextParam = False
    global newDec
    global declaring
    global onLine
    skip = 0
    for line in code:
        if newDec:
            if newDec.type == 'function':
                funcs.append(newDec)
            elif newDec.type:
                vars.append(newDec)
        newDec = 0
        declaring = False
        assigning = False
        codeToFunc = False
        onLine = onLine + 1
        for char in newChars:
            line = line.replace(char, f' {char} ')
        print(line)
        line = line.split()
        for term in line:
            if skip != 1:
                print(term)
                if term == '#':
                    skip = 1
                    continue
                if term in terms and declaring == False:
                    declare(term, onLine)
                elif term == 'be' and newDec.type != 'function':
                    assigning = True
                elif declaring:
                    if not newDec.name and not term in terms:
                        newDec.name = term
                    else:
                        if newDec.type == 'function':
                            if term == '(':
                                addParams = True
                                nextParam = True
                            elif term == ')':
                                if not nextParam:
                                    addParams = False
                                    nextParam = False
                                else:
                                    error(onLine, line, 'badComma')
                            elif term ==',':
                                nextParam = True
                            elif term == '{':
                                if not nextParam:
                                    pass
                                else:
                                    error(onLine, line , 'badComma')
                            elif term not in terms and addParams and nextParam:
                                nextParam = False
                                newDec.params.append(term)
                        elif assigning:
                            newDec.value = term
                        else:
                            error(onLine, line, 'declaration')
                else:
                    error(onLine, line, 'notDefined', term)

    print(code, vars, funcs)
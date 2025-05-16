import error as err

ignore = ['#', ';']
newChars = ['(', ')', '{', '}', ',', '#', '\'', '"']
vars = []
funcs = []
terms = ['bid', 'exalt', 'hark', 'be', 'eternal', 'doth', 'with', 'without']
declares = ['bid', 'eternal', 'doth']

def declare(term, line):
    global declaring
    global newDec
    if term in declares:
        if declaring:
            err.error(line, None, 'unexpected', term)
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
    def __init__(self, line=0, name=0, params=[], script=[]):
        self.type = 'function'
        self.line = line
        self.name = name
        self.params = params
        self.script = script
        
    def runScript(self):
        pass
    
newDec = Variable()

declaring = False
onLine = 0

def run(code):
    assigning = False
    addParams = False
    nextParam = False
    global newDec
    global declaring
    global onLine
    global codeToFunc
    codeToFunc = False
    global printing
    printing = False
    skip = 0
    for line in code:
        if newDec and not codeToFunc:
            if newDec.type == 'function':
                funcs.append(newDec)
            elif newDec.type:
                vars.append(newDec)
        if not codeToFunc:
            declaring = False
            newDec = 0
        assigning = False
        onLine = onLine + 1
        for char in newChars:
            line = line.replace(char, f' {char} ')
        line = line.split()
        if codeToFunc and newDec.type == 'function':
            if not '}' in line:
                newDec.script.append(line)
            elif len(line) > 1:
                err.error(onLine, line, 'badClose')
            else:
                codeToFunc = False
        for term in line:
            if skip != 1:
                if term == '#':
                    skip = 1
                    continue
                if term in declares and declaring == False:
                    declare(term, onLine)
                elif term == 'be' and newDec.type != 'function':
                    assigning = True
                elif declaring:
                    if not newDec.name and not term in terms:
                        newDec.name = term
                    else:
                        if newDec.type == 'function':
                            if not codeToFunc:
                                if term == '(':
                                    addParams = True
                                    nextParam = True
                                elif term == ')':
                                    if not nextParam:
                                        addParams = False
                                        nextParam = False
                                    else:
                                        err.error(onLine, line, 'badComma')
                                elif term ==',':
                                    nextParam = True
                                elif term == '{':
                                    if not nextParam:
                                        codeToFunc = True
                                    else:
                                        err.error(onLine, line , 'badComma')
                                elif term not in terms and addParams and nextParam:
                                    nextParam = False
                                    newDec.params.append(term)
                        elif assigning:
                            newDec.value = term
                        else:
                            err.error(onLine, line, 'declaration')
                elif term == 'hark':
                    printing = True
                else:
                    err.error(onLine, line, 'notDefined', term)

    print('Variables:')
    for var in vars:
        print(f'(Declared on line {var.line}) - {var.type} {var.name} = {var.value}')
    print('Functions:')
    for func in funcs:
        print(f'(Declared on line {func.line}) - {func.name}({", ".join(func.params)})')
        for line in func.script:
            print(f'  {line}')
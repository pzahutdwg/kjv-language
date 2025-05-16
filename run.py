import error as err
def quit(status, line=None, wholeLine=None, type=None, term=None):
    if status == 1:
        err.error(line, wholeLine, type, term)
        
    print('Variables:')
    for var in vars:
        print(f'(Declared on line {var.line}) - {var.type} {var.name} = {var.value} (eternal: {var.eternal})')
    print('Functions:')
    for func in funcs:
        print(f'(Declared on line {func.line}) - {func.name}({", ".join(func.params)})')
        for line in func.script:
            print(f'  {' '.join(line)}')
    
    exit(status)
ignore = ['#', ';']
newChars = ['(', ')', '{', '}', ',', '#', '\'', '"']
vars = []
funcs = []
terms = ['measure', 'exalt', 'hark', 'be', 'eternal', 'doth', 'with', 'without']
declares = ['measure', 'eternal', 'doth', 'utterance']

def declare(term, line):
    global declaring
    global newDec
    if term in declares:
        if declaring:
            quit(1, line, None, 'unexpected', term)
        else:
            declaring = True
            if term == 'doth':
                newDec = Function(line)
            elif term != 'eternal':
                newDec = Variable(line, term)
            else:
                newDec = Variable(line, None, None, None, True)

def printVal(line):
    global skip
    skip = 1
    val = ''
    string = False
    for term in line:
        if term == 'hark':
            continue
        if not string:
            if term == '"':
                string = True
                continue
            else:
                for func in funcs:
                    if term == func.name:
                        val = val + func.runScript()
                        break
        else:
            if term == '"':
                string = False
                continue
            else:
                val = val + ' ' + str(term)
            
    print(val)

class Variable():
    def __init__(self, line=None, type=None, name=None, value=None, eternal=False):
        self.line = line
        self.type = type
        self.name = name
        self.value = value
        self.eternal = eternal
        
class Function():
    def __init__(self, line=None, name=None, params=[], script=[]):
        self.type = 'function'
        self.line = line
        self.name = name
        self.params = params
        self.script = script
        
    def runScript(self):
        print(self.name, 'running.')
    
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
    global skip
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
                quit(1, onLine, line, 'badClose')
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
                    elif not newDec.type and term in declares and not term == 'eternal':
                        newDec.type = term
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
                                        quit(1, onLine, line, 'badComma')
                                elif term ==',':
                                    nextParam = True
                                elif term == '{':
                                    if not nextParam:
                                        codeToFunc = True
                                    else:
                                        quit(1, onLine, line , 'badComma')
                                elif term not in terms and addParams and nextParam:
                                    nextParam = False
                                    newDec.params.append(term)
                        elif assigning:
                            if newDec.type != 'utterance':
                                newDec.value = term
                            else:
                                if newDec.value:
                                    newDec.value = str(newDec.value) + ' ' + str(term)
                                else:
                                    newDec.value = term
                        else:
                            quit(1, onLine, line, 'declaration')
                elif term == 'hark':
                    printing = True
                    printVal(line)
                else:
                    quit(1, onLine, line, 'notDefined', term)
            
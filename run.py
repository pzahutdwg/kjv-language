ignore = ['#', ';']
newChars = ['(', ')', '{', '}', ',', '#']
vars = []
funcs = []
terms = ['bid', 'exalt', 'hark', 'be', 'eternal', 'doth', 'with', 'without']

def doStuff(term):
    pass

def error():
    pass

class Declaration:
    def __init__(self, line, type, name):
        self.line = line
        self.type = type
        self.name = name
        
class Function(Declaration):
    def __init__(self, line, type, name, params, script):
        super().__init__(line, type, name)
        self.params = params
        self.script = script
        
    def runScript(self):
        pass

declaring = False

def run(code):
    skip = 0
    for line in code:
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
                if term in 'terms' and declaring == False:
                    doStuff(term)
                elif declaring:
                    pass
                else:
                    error()

    print(code)
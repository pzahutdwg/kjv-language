ignore = ['#', ';']
newChars = ['(', ')', '{', '}', ',']
vars = []
funcs = []

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

def run(code):
    for line in code:
        print(line)
        line = line.split()
        for term in line:
            print(term)
            for char in term:
                if char == '#':
                    pass
    print(code)
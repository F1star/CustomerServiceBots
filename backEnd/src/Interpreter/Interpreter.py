from DataStructure import UserTable

class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.userTable = UserTable(tree.getVarName())
        self.mainStep = tree.getMainStep()

    def dispatch(self):
        curStep = self.tree.getStep()[self.mainStep]
        for state in curStep:
            if state[0] == 'Speak':
                self.doSpeak(state)
            elif state[0] == 'Listen':
                self.doListen(state)

    def doSpeak(self, state):
        expression = ''
        for i in range(1, len(state)):
            if state[i] in self.tree.getVarName():
                expression += self.userTable.getTable()[state[i]]
            else:
                expression += state[i]
        print(expression)
    
    def doListen(self, state):
        pass
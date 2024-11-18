from src.Interpreter.DataStructure import Root, Step, Expression


class Grammar:
    def __init__(self, tokens):
        self.tokens = tokens
        self.grmTree = Root()
        self.step = Step()
        self.expr = Expression()
        self.isAppend = False  # Branch 是否已经追加到 step 中
        self.processTokens()

    def processTokens(self):
        for token in self.tokens:
            if token[0] == "Step":
                self.processStep(token)
            elif token[0] == "Speak":
                self.processSpeak(token)
            elif token[0] == "Expression":
                self.processExpression(token)
            elif token[0] == "Listen":
                self.processListen(token)
            elif token[0] == "Branch":
                self.processBranch(token)
            elif token[0] == "Silence":
                self.processSilence(token)
            elif token[0] == "Default":
                self.processDefault(token)
            elif token[0] == "Exit":
                self.processExit(token)
            else:
                print("Unknown token type:", token[0])
                break

        self.appendToTree()

    def appendToTree(self):
        self.grmTree.addStep(self.step.getStepID(), self.step.getStep())
        self.step = Step()
        self.isAppend = False
    
    def appendExpr(self, token, num):
        for i in range(num):
            self.expr.addExpr(token[i])
        self.step.addStep(self.expr.getExpr())
        self.expr = Expression()

    def processStep(self, token):
        if len(token) < 2:
            self.processError(token)
            return
        if self.grmTree.getMainStep() is None:
            self.grmTree.setMainStep(token[1])
        else:
            self.appendToTree()

        self.step.setStepID(token[1])

    def processSpeak(self, token):
        self.processExpression(token)
        self.step.addStep(self.expr.getExpr())
        self.expr = Expression()

    def processExpression(self, token):
        self.expr.addExpr(token[0])
        for i in range(1, len(token)):
            if token[i] == '+':
                continue
            elif token[i][0] == '$':
                self.grmTree.addVarName(token[i][1:])
                self.expr.addExpr(token[i][1:])
            elif token[i][0] == '"' and token[i][-1] == '"':
                self.expr.addExpr(token[i][1:-1])
            else:
                self.processError(token[i])


    def processListen(self, token):
        if len(token) != 2:
            self.processError(token)
        self.appendExpr(token, len(token))


    def processBranch(self, token):
        if len(token) != 3:
            self.processError(token)
        if self.isAppend == False:
            self.appendExpr(token, 1)
            self.isAppend = True
        self.grmTree.addBranch(token[1][1:-1], token[2])  


    def processSilence(self, token):
        if len(token) != 2:
            self.processError(token)
        self.appendExpr(token, len(token))

    def processDefault(self, token):
        if len(token) != 2:
            self.processError(token)
        self.appendExpr(token, len(token))

    def processExit(self, token):
        if len(token) > 1:
            self.processError(token)
        self.appendExpr(token, len(token))

    @staticmethod
    def processError(token):
        print(f"Error: Invalid token{token}")

    def getGrmTree(self):
        return self.grmTree


class Root:
    def __init__(self):
        self.stepTable = dict()
        self.mainStep = None
        self.name = ''
        self.varName = []
        self.branchTable = dict()

    def getStep(self):
        return self.stepTable

    def getMainStep(self):
        return self.mainStep

    def getName(self):
        return self.name

    def setMainStep(self, mainStep):
        self.mainStep = mainStep

    def setName(self, name):
        self.name = name

    def addStep(self, stepID, step):
        self.stepTable[stepID] = step

    def addVarName(self, varName):
        if varName not in self.varName:
            self.varName.append(varName)
    
    def getVarName(self):
        return self.varName
    
    def getBranch(self):
        return self.branchTable
    
    def addBranch(self, branchID, branch):
        self.branchTable[branchID] = branch



class Step:
    def __init__(self):
        self.stepID = None
        self.step = []

    def getStepID(self):
        return self.stepID

    def getStep(self):
        return self.step

    def setStepID(self, stepID):
        self.stepID = stepID

    def addStep(self, step):
        self.step.append(step)



class Expression:
    def __init__(self):
        self.expr = []

    def addExpr(self, expr):
        self.expr.append(expr)

    def getExpr(self):
        return self.expr
    

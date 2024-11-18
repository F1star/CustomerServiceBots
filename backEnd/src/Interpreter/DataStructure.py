class Root:
    def __init__(self):
        """初始化根类的各个属性"""
        self.stepTable = dict()  # 步骤表，存储步骤ID和步骤内容
        self.mainStep = None  # 主要步骤
        self.varName = []  # 存储变量名
        self.branchTable = dict()  # 分支表，存储分支ID和分支内容

    def getStep(self):
        """获取步骤表"""
        return self.stepTable

    def getMainStep(self):
        """获取主要步骤"""
        return self.mainStep

    def getName(self):
        """获取名称"""
        return self.name

    def setMainStep(self, mainStep):
        """设置主要步骤"""
        self.mainStep = mainStep

    def setName(self, name):
        """设置名称"""
        self.name = name

    def addStep(self, stepID, step):
        """向步骤表中添加步骤"""
        self.stepTable[stepID] = step

    def addVarName(self, varName):
        """添加变量名到变量列表中，避免重复"""
        if varName not in self.varName:
            self.varName.append(varName)
    
    def getVarName(self):
        """获取所有变量名"""
        return self.varName
    
    def getBranch(self):
        """获取分支表"""
        return self.branchTable
    
    def addBranch(self, branchID, branch):
        """向分支表中添加分支"""
        self.branchTable[branchID] = branch



class Step:
    def __init__(self):
        """初始化步骤类的属性"""
        self.stepID = None  # 步骤ID
        self.step = []  # 步骤内容列表

    def getStepID(self):
        """获取步骤ID"""
        return self.stepID

    def getStep(self):
        """获取步骤内容"""
        return self.step

    def setStepID(self, stepID):
        """设置步骤ID"""
        self.stepID = stepID

    def addStep(self, step):
        """向步骤内容列表中添加步骤"""
        self.step.append(step)



class Expression:
    def __init__(self):
        """初始化表达式类的属性"""
        self.expr = []  # 存储表达式的列表

    def addExpr(self, expr):
        """向表达式列表中添加表达式"""
        self.expr.append(expr)

    def getExpr(self):
        """获取所有表达式"""
        return self.expr
    

class UserTable:
    def __init__(self, varName):
        """初始化用户表类的属性"""
        self.userTable = dict()  # 用户表，存储用户信息
        self.varName = varName  # 变量名

    def setName(self, name):
        """设置用户名称"""
        self.userTable['name'] = name

    def setUser(self, infoName, userInfo):
        """设置用户信息"""
        self.userTable[infoName] = userInfo

    def getTable(self):
        """获取用户表"""
        return self.userTable

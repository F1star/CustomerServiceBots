from src.Interpreter.DataStructure import Root, Step, Expression


class Grammar:
    def __init__(self, tokens):
        """
        初始化，接收tokens并创建语法树、步骤和表达式
        """
        self.tokens = tokens
        self.grmTree = Root()  # 语法树根节点
        self.step = Step()  # 当前步骤
        self.expr = Expression()  # 当前表达式
        self.isAppend = False  # 标记是否已经追加Branch
        self.processTokens()  # 开始处理tokens

    def processTokens(self):
        """
        遍历所有tokens，根据类型调用不同的处理函数
        """
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
                # 如果遇到未知类型的token，输出错误并停止处理
                print("Unknown token type:", token[0])
                break
        self.appendToTree()  # 处理完tokens后，追加到语法树

    def appendToTree(self):
        """
        将当前步骤添加到语法树并重置步骤对象
        """
        self.grmTree.addStep(self.step.getStepID(), self.step.getStep())
        self.step = Step()  # 重置步骤对象
        self.isAppend = False  # 重置标记

    def appendExpr(self, token, num):
        """将表达式的内容添加到当前步骤"""
        for i in range(num):
            self.expr.addExpr(token[i])
        self.step.addStep(self.expr.getExpr())  # 将表达式加入步骤
        self.expr = Expression()  # 重置表达式对象

    def processStep(self, token):
        """处理Step类型的token"""
        if len(token) < 2:
            self.processError(token)  # 如果token不合法，抛出错误
            return
        if self.grmTree.getMainStep() is None:
            self.grmTree.setMainStep(token[1])  # 设置主步骤
        else:
            self.appendToTree()  # 如果已经有主步骤，追加到树中
        self.step.setStepID(token[1])  # 设置当前步骤ID

    def processSpeak(self, token):
        """
        处理Speak类型的token，Speak类型的流程包含表达式
        """
        self.processExpression(token)  # 解析表达式
        self.step.addStep(self.expr.getExpr())  # 将表达式添加到步骤
        self.expr = Expression()  # 重置表达式对象

    def processExpression(self, token):
        """
        处理Expression类型的token
        """
        self.expr.addExpr(token[0])  # 添加第一个词法单元到表达式
        for i in range(1, len(token)):
            if token[i] == '+': continue  # 跳过 '+' 符号
            elif token[i][0] == '$': 
                self.grmTree.addVarName(token[i][1:])  # 添加变量到语法树
                self.expr.addExpr(token[i][1:])  # 将变量名加入表达式
            elif token[i][0] == '"' and token[i][-1] == '"': 
                self.expr.addExpr(token[i][1:-1])  # 去掉引号并加入表达式
            else:
                self.processError(token[i])  # 其他不合法token抛出错误

    def processListen(self, token):
        """
        处理Listen类型的token，表示一个等待步骤
        """
        if len(token) != 2:
            self.processError(token)  # 长度不合法，抛出错误
        self.appendExpr(token, len(token))  # 将token添加为表达式并加入步骤

    def processBranch(self, token):
        """
        处理Branch类型的token，表示一个分支
        """
        if len(token) != 3:
            self.processError(token)  # 长度不合法，抛出错误
        if not self.isAppend:
            self.appendExpr(token, 1)  # 分支前必须有一个表达式
            self.isAppend = True  # 标记分支已添加
        self.grmTree.addBranch(token[1][1:-1], token[2])  # 添加分支到语法树

    def processSilence(self, token):
        """
        处理Silence类型的token，表示静默步骤
        """
        if len(token) != 2:
            self.processError(token)  # 长度不合法，抛出错误
        self.appendExpr(token, len(token))  # 将token作为表达式加入步骤

    def processDefault(self, token):
        """处理Default类型的token，表示默认操作"""
        if len(token) != 2:
            self.processError(token)  # 长度不合法，抛出错误
        self.appendExpr(token, len(token))  # 将token作为表达式加入步骤

    def processExit(self, token):
        """处理Exit类型的token，表示退出操作"""
        if len(token) > 1:
            self.processError(token)  # 长度不合法，抛出错误
        self.appendExpr(token, len(token))  # 将token作为表达式加入步骤

    @staticmethod
    def processError(token):
        """输出错误信息"""
        print(f"Error: Invalid token {token}")

    def getGrmTree(self):
        """获取语法树对象"""
        return self.grmTree

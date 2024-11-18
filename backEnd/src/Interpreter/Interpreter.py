import threading
from src.Interpreter.DataStructure import UserTable

class Interpreter:
    def __init__(self, tree):
        """
        初始化解释器，接收语法树并设置必要的变量。
        """
        self.tree = tree  # 语法树
        self.userTable = UserTable(tree.getVarName())  # 用户数据表，存储变量
        self.mainStep = tree.getMainStep()  # 主步骤
        self.curStep = None  # 当前步骤
        self.userInput = None  # 用户输入
        self.inputEvent = threading.Event()  # 线程事件，用于等待输入
        self.resultLock = threading.Lock()  # 线程锁，确保对latest_result的线程安全访问
        self.latestResult = None  # 最新结果缓存

    def setName(self, name):
        """设置用户名称"""
        self.userTable.setName(name)

    def setInfo(self, InfoName, userInfo):
        """设置用户信息"""
        self.userTable.setUser(InfoName, userInfo)

    def getInfo(self):
        """获取所有变量名"""
        return self.tree.getVarName()

    def setUserInput(self, userInput):
        """设置用户输入并触发事件"""
        self.userInput = userInput
        self.inputEvent.set()  # 设置事件，表示用户输入已准备好

    def getLatestResult(self):
        """获取并清除最新结果"""
        with self.resultLock:
            result = self.latestResult
            self.latestResult = None  # 读取后清空最新结果
            return result

    def dispatch(self):
        """
        根据语法树执行步骤调度，处理不同的状态。
        """
        stepName = self.mainStep  # 从主步骤开始
        isInTime = False  # 是否在合适的时间点进行分支
        while stepName:
            self.curStep = self.tree.getStep()[stepName]  # 获取当前步骤
            flag = False  # 标记，用于跳过无效步骤

            for state in self.curStep:
                if state[0] == 'Speak':
                    self.doSpeak(state)  # 执行说话操作
                elif state[0] == 'Listen':
                    isInTime = self.doListen(state)  # 执行监听操作
                elif state[0] == 'Branch':
                    if isInTime:
                        # 处理分支，根据用户输入决定跳转到哪个步骤
                        keyList = list(self.tree.getBranch().keys())
                        isBreak = False
                        for i in range(len(self.tree.getBranch())):
                            if keyList[i] in self.userInput:
                                stepName = self.tree.getBranch()[keyList[i]]
                                isBreak = True
                                break
                        if isBreak:
                            break
                        else:
                            flag = True
                    else:
                        continue
                elif state[0] == 'Silence':
                    # 如果没有分支需要跳转，继续执行下一个步骤
                    if flag:
                        flag = False
                        continue
                    stepName = state[1]  # 跳转到下一个步骤
                    break
                elif state[0] == 'Default':
                    stepName = state[1]  # 执行默认步骤
                    break
                elif state[0] == 'Exit':
                    return  # 执行退出操作，结束执行

    def doSpeak(self, state):
        """
        执行输出语句，拼接表达式并输出。
        """
        expression = ''
        for i in range(1, len(state)):
            # 替换表达式中的变量
            if state[i] in self.tree.getVarName():
                expression += self.userTable.getTable()[state[i]]
            else:
                expression += state[i]  # 如果不是变量，直接拼接
        print(expression)  # 输出表达式
        with self.resultLock:
            self.latestResult = expression  # 保存最新结果
        return

    def doListen(self, state):
        """
        执行监听操作，等待用户输入。
        """
        self.userInput = None
        self.inputEvent.clear()  # 清除输入事件标志，等待用户输入
        isInTime = self.getInput(int(state[1]))  # 等待输入，超时后返回
        return isInTime

    def getInput(self, timeout):
        """
        等待用户输入，超时则返回False。
        """
        isSet = self.inputEvent.wait(timeout)  # 等待用户输入事件触发
        if isSet:
            print(f"用户输入：{self.userInput}")
            return True  # 用户输入有效
        else:
            print("超时")
            return False  # 超时未输入

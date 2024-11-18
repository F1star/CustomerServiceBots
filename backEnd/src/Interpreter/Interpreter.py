import threading
from src.Interpreter.DataStructure import UserTable

class Interpreter:
    def __init__(self, tree):
        """
        初始化解释器对象，接收语法树并准备执行相关操作。
        """
        self.tree = tree
        self.userTable = UserTable(tree.getVarName())
        self.mainStep = tree.getMainStep()
        self.curStep = None
        self.userInput = None
        self.input_event = threading.Event()
        self.result_lock = threading.Lock()
        self.latest_result = None

    def setName(self, name):
        self.userTable.setName(name)

    def setInfo(self, InfoName, userInfo):
        self.userTable.setUser(InfoName, userInfo)

    def getInfo(self):
        return self.tree.getVarName()

    def setUserInput(self, userInput):
        self.userInput = userInput
        self.input_event.set()

    def getLatestResult(self):
        with self.result_lock:
            result = self.latest_result
            self.latest_result = None  # 读取后清除最新结果
            return result

    def dispatch(self):
        """
        根据语法树执行步骤调度。
        """
        stepName = self.mainStep
        isInTime = False
        while stepName:
            self.curStep = self.tree.getStep()[stepName]
            flag = False

            for state in self.curStep:
                if state[0] == 'Speak':
                    self.doSpeak(state)
                elif state[0] == 'Listen':
                    isInTime = self.doListen(state)
                elif state[0] == 'Branch':
                    if isInTime:
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
                    if flag:
                        flag = False
                        continue
                    stepName = state[1]
                    break
                elif state[0] == 'Default':
                    stepName = state[1]
                    break
                elif state[0] == 'Exit':
                    return

    def doSpeak(self, state):
        """
        执行输出语句。
        """
        expression = ''
        for i in range(1, len(state)):
            if state[i] in self.tree.getVarName():
                expression += self.userTable.getTable()[state[i]]
            else:
                expression += state[i]
        print(expression)
        with self.result_lock:
            self.latest_result = expression
        return

    def doListen(self, state):
        """
        执行监听操作，等待用户输入。
        """
        self.userInput = None
        self.input_event.clear()
        isInTime = self.getInput(int(state[1]))
        return isInTime

    def getInput(self, timeout):
        """
        等待用户输入，使用线程进行超时控制。
        """
        is_set = self.input_event.wait(timeout)
        if is_set:
            print(f"用户输入：{self.userInput}")
            return True
        else:
            print("超时")
            return False

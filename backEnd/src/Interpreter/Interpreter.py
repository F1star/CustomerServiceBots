import threading
import msvcrt
import time
from src.Interpreter.DataStructure import UserTable

class Interpreter:
    def __init__(self, tree):
        """
        初始化解释器对象，接收语法树并准备执行相关操作。
        """
        self.tree = tree  # 保存语法树对象
        self.userTable = UserTable(tree.getVarName())  # 初始化用户表，获取变量名称
        self.mainStep = tree.getMainStep()  # 获取主步骤
        self.curStep = None  # 当前步骤初始化为 None
        self.userInput = None  # 用户输入初始化为 None

    def dispatch(self):
        """
        根据语法树执行步骤调度。通过树中的步骤和分支控制流程。
        """
        stepName = self.mainStep  # 初始化步骤名为主步骤
        isInTime = False  # 用于记录是否在规定时间内接收到输入
        while stepName:
            # 获取当前步骤，树中存储步骤名到步骤内容的映射
            self.curStep = self.tree.getStep()[stepName]
            
            count = 0
            # 遍历当前步骤中的所有状态
            for state in self.curStep:
                if state[0] == 'Speak':
                    self.doSpeak(state)  # 如果状态是Speak，执行输出
                elif state[0] == 'Listen':
                    isInTime = self.doListen(state)  # 如果状态是Listen，等待输入并判断是否超时
                elif state[0] == 'Branch':
                    # 根据是否超时进行分支跳转
                    if isInTime:
                        # 如果输入有效且有对应的分支，跳转到相应的步骤
                        if self.tree.getBranch().get(str(self.userInput)) is not None:
                            stepName = self.tree.getBranch()[str(self.userInput)]
                            break
                        else:
                            # 如果没有对应的分支，则跳转到默认步骤
                            count += 1
                    else:
                        # 如果超时，跳过当前分支
                        continue
                elif state[0] == 'Silence':
                    # 如果状态是Silence，直接跳转到指定步骤
                    if count > 0:
                        count -= 1
                        continue
                    stepName = state[1]
                    break
                elif state[0] == 'Default':
                    stepName = state[1]
                    break
                elif state[0] == 'Exit':
                    return  # 如果状态是Exit，退出程序

    
    def doSpeak(self, state):
        """
        执行输出语句。根据语法树中的变量名进行替换并打印输出。
        """
        expression = ''
        # 遍历Speak指令的参数，进行替换并生成最终的输出字符串
        for i in range(1, len(state)):
            if state[i] in self.tree.getVarName():
                # 如果该参数是变量名，则从用户表中获取相应的值
                expression += self.userTable.getTable()[state[i]]
            else:
                # 否则直接输出该参数
                expression += state[i]
        print(expression)  # 输出生成的表达式
    
    def doListen(self, state):
        """
        执行监听操作，等待用户输入。超时后返回 False，输入有效则返回 True。
        """
        isInTime = self.getInput(int(state[1]))  # 获取用户输入并判断是否超时
        return isInTime  # 返回是否在规定时间内输入了有效内容

    def getInput(self, timeout):
        """
        等待用户输入，使用线程进行超时控制。如果用户在指定时间内没有输入，返回 False。
        否则返回用户输入的内容。
        """
        inputEvent = threading.Event()

        def waitInput():
            """
            线程中执行等待用户输入的操作。
            """
            print(f"请输入（{timeout}秒内投诉请按1，账单请按2，其他请按0）：", end="", flush=True)
            start_time = time.time()
            while time.time() - start_time < timeout:
                if msvcrt.kbhit():  # 检查键盘是否有按键输入
                    byte_input = msvcrt.getch()  # 获取输入的字节
                    self.userInput = chr(byte_input[0])  # 将字节转换为字符
                    inputEvent.set()  # 设置事件标记为已完成
                    break
                time.sleep(0.1)  # 每次循环后稍等，防止占用过多 CPU

        # 创建并启动获取输入的线程
        inputThread = threading.Thread(target=waitInput)
        inputThread.daemon = True  # 设置为守护线程，主线程结束时自动结束
        inputThread.start()

        # 主线程等待输入线程在规定时间内完成
        inputThread.join(timeout)

        # 判断是否在规定时间内有输入
        if inputEvent.is_set():
            if self.userInput == '1':
                self.userInput = '投诉'
            elif self.userInput == '2':
                self.userInput = '账单'
            else:
                self.userInput = '其他'
            print(f"用户输入：{self.userInput}")
            return True
        else:
            print("超时")  # 如果超时，打印超时信息
            return False

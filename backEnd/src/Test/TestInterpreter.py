import unittest
import threading
from src.Interpreter.Interpreter import Interpreter
from src.Interpreter.Grammar import Grammar

class TestInterpreter(unittest.TestCase):
    """
    测试Interpreter类的功能，包括Speak、Listen和Silence的执行。
    """
    def setUp(self):
        """
        初始化测试数据，包括模拟的tokens，语法树（Grammar）和解释器（Interpreter）对象。
        """
        tokens = [
            ['Step', 'main'],
            ['Speak', '"Hello World"'],
            ['Listen', '5'],
            ['Branch', '"yes"', 'yes_step'],
            ['Silence', 'no_response'],
            ['Step', 'yes_step'],
            ['Speak', '"You said yes"'],
            ['Exit'],
            ['Step', 'no_response'],
            ['Speak', '"No response received"'],
            ['Exit']
        ]
        self.grammar = Grammar(tokens)
        self.grmTree = self.grammar.getGrmTree()
        self.interpreter = Interpreter(self.grmTree)

    def testInterpreterSpeak(self):
        """
        测试Interpreter的Speak功能，确保正确输出指定的语句。
        """
        # 捕获输出
        from io import StringIO
        import sys
        capturedOutput = StringIO()
        sys.stdout = capturedOutput

        # 启动解释器线程
        threading.Thread(target=self.interpreter.dispatch).start()

        # 等待一定时间以确保输出
        import time
        time.sleep(0.5)  # 等待0.5秒

        sys.stdout = sys.__stdout__  # 恢复标准输出
        output = capturedOutput.getvalue().strip()

        # 验证输出是否包含预期的语句
        self.assertIn("Hello World", output)

    def testInterpreterListenAndBranch(self):
        """
        测试Interpreter的Listen和Branch功能，确保输入后正确进入相应的分支。
        """
        # 模拟用户输入
        def provideInput():
            import time
            time.sleep(0.2)
            self.interpreter.setUserInput("yes")

        threading.Thread(target=provideInput).start()

        # 捕获输出
        from io import StringIO
        import sys
        capturedOutput = StringIO()
        sys.stdout = capturedOutput

        # 启动解释器
        self.interpreter.dispatch()

        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue().strip()

        # 验证输出是否包含预期语句
        self.assertIn("Hello World", output)
        self.assertIn("You said yes", output)

    def testInterpreterSilence(self):
        """
        测试Interpreter的Silence功能，确保在没有输入时正确输出无响应消息。
        """
        # 捕获输出
        from io import StringIO
        import sys
        capturedOutput = StringIO()
        sys.stdout = capturedOutput

        # 启动解释器
        self.interpreter.dispatch()

        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue().strip()

        # 验证输出是否包含无响应的消息
        self.assertIn("No response received", output)

if __name__ == '__main__':
    unittest.main()  # 执行测试

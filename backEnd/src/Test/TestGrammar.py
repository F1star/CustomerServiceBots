import unittest
from src.Interpreter.Grammar import Grammar

class TestGrammar(unittest.TestCase):
    """
    测试Grammar类的功能，包括语法树构建、变量名处理及错误处理
    """
    def setUp(self):
        """初始化测试数据并创建Grammar对象"""
        self.tokens = [
            ['Step', 'main'],
            ['Speak', '"Hello World"'],
            ['Listen', '5'],
            ['Exit']
        ]
        self.grammar = Grammar(self.tokens)  # 创建Grammar实例

    def testGrammarTree(self):
        """测试语法树的构建，验证主步骤和步骤内容"""
        grmTree = self.grammar.getGrmTree()
        
        # 验证主步骤是否正确
        self.assertEqual(grmTree.getMainStep(), 'main')
        
        # 验证步骤内容是否正确
        steps = grmTree.getStep()
        self.assertIn('main', steps)  # 确认主步骤在步骤表中
        
        # 验证主步骤的内容是否正确
        stepContent = steps['main']
        expectedStepContent = [
            ['Speak', 'Hello World'],
            ['Listen', '5'],
            ['Exit']
        ]
        self.assertEqual(stepContent, expectedStepContent)

    def testVariableNames(self):
        """测试变量名处理，确保语法树能够识别并存储变量名"""
        tokensWithVars = [
            ['Step', 'main'],
            ['Speak', '"Hello World"'],
            ['Speak', '$name'],  # 包含变量
            ['Exit']
        ]
        grammar = Grammar(tokensWithVars)  # 创建新的Grammar对象
        grmTree = grammar.getGrmTree()
        
        # 验证变量名是否被正确提取
        varNames = grmTree.getVarName()
        self.assertIn('name', varNames)  # 检查变量名是否在列表中

    def testProcessError(self):
        """测试语法解析中的错误处理，确保无效token会产生错误输出"""
        tokensWithError = [
            ['Step'],  # 缺少步骤名称
            ['Speak', 'Hello']
        ]
        
        # 捕获错误输出
        from io import StringIO
        import sys
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        
        # 创建Grammar对象并触发错误
        grammar = Grammar(tokensWithError)
        
        # 恢复标准输出流
        sys.stdout = sys.__stdout__
        
        # 验证错误消息是否包含"Invalid token"
        output = capturedOutput.getvalue().strip()
        self.assertIn("Error: Invalid token", output)

if __name__ == '__main__':
    unittest.main()  # 执行测试

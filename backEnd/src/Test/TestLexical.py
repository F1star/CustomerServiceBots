import unittest
import os
from src.Interpreter.Lexical import Lexical

class TestLexical(unittest.TestCase):
    """
    测试Lexical类的词法分析功能
    """
    def setUp(self):
        """创建临时测试文件，用于词法分析测试"""
        self.testFileName = 'test_input.txt'
        with open(self.testFileName, 'w', encoding='utf-8') as f:
            f.write('Step main\n')  # 步骤定义
            f.write('Speak "Hello World"\n')  # 输出语句
            f.write('Listen 5\n')  # 听取输入
            f.write('# This is a comment\n')  # 注释行
            f.write('\n')  # 空行

    def tearDown(self):
        """测试完成后删除临时文件"""
        os.remove(self.testFileName)
    
    def testLexicalParsing(self):
        """测试Lexical类的词法解析功能"""
        lexer = Lexical(self.testFileName)
        tokens = lexer.getTokens()  # 获取词法单元
        expectedTokens = [
            ['Step', 'main'],
            ['Speak', '"Hello World"'],
            ['Listen', '5']
        ]
        self.assertEqual(tokens, expectedTokens)  # 验证词法单元是否与预期一致
    
    def testPrintTokens(self):
        """测试Lexical类的printTokens方法输出"""
        lexer = Lexical(self.testFileName)
        
        # 捕获printTokens的输出
        from io import StringIO
        import sys
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        lexer.printTokens()  # 调用打印方法
        sys.stdout = sys.__stdout__  # 恢复原输出流
        
        # 获取并比较输出内容
        output = capturedOutput.getvalue().strip().split('\n')
        expectedOutput = [
            "['Step', 'main']",
            "['Speak', '\"Hello World\"']",
            "['Listen', '5']"
        ]
        self.assertEqual(output, expectedOutput)  # 验证输出是否与预期一致

if __name__ == '__main__':
    unittest.main()  # 运行测试

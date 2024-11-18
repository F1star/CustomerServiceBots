# testLexical.py

import unittest
import os
from src.Interpreter.Lexical import Lexical

class TestLexical(unittest.TestCase):
    def setUp(self):
        # 创建一个临时测试文件
        self.testFileName = 'test_input.txt'
        with open(self.testFileName, 'w', encoding='utf-8') as f:
            f.write('Step main\n')
            f.write('Speak "Hello World"\n')
            f.write('Listen 5\n')
            f.write('# This is a comment\n')
            f.write('\n')  # 空行

    def tearDown(self):
        # 删除临时文件
        os.remove(self.testFileName)
    
    def testLexicalParsing(self):
        lexer = Lexical(self.testFileName)
        tokens = lexer.getTokens()
        expectedTokens = [
            ['Step', 'main'],
            ['Speak', '"Hello World"'],
            ['Listen', '5']
        ]
        self.assertEqual(tokens, expectedTokens)
    
    def testPrintTokens(self):
        lexer = Lexical(self.testFileName)
        # 捕获打印输出
        from io import StringIO
        import sys
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        lexer.printTokens()
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue().strip().split('\n')
        expectedOutput = ["['Step', 'main']", "['Speak', '\"Hello World\"']", "['Listen', '5']"]
        self.assertEqual(output, expectedOutput)

if __name__ == '__main__':
    unittest.main()

import unittest
from src.Interpreter.Lexical import Lexical

class TestLexical(unittest.TestCase):
    def testParserFile(self):
        # 创建一个临时的脚本文件
        test_script = "src/Test/testScript.txt"
        with open(test_script, "w", encoding="utf-8") as f:
            f.write("""
            # This is a comment
            Step MainStep
            Speak "Hello, World!"
            Listen 5
            Branch "Option1" Step1
            # Another comment
            Exit
            """)
        
        lexical = Lexical(test_script)
        tokens = lexical.getTokens()
        
        expected_tokens = [
            ['Step', 'MainStep'],
            ['Speak', '"Hello,', 'World!"'],
            ['Listen', '5'],
            ['Branch', '"Option1"', 'Step1'],
            ['Exit']
        ]
        self.assertEqual(tokens, expected_tokens)

if __name__ == "__main__":
    unittest.main()

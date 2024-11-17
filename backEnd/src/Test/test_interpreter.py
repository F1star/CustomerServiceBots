import unittest
from unittest.mock import patch, MagicMock
from src.Interpreter.DataStructure import Root, UserTable
from src.Interpreter.Interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    @patch('builtins.input', side_effect=["Charlie"])
    @patch('msvcrt.getch', side_effect=[b'1'])
    def test_dispatch(self, mock_getch, mock_input):
        # 构建语法树
        root = Root()
        root.setMainStep("MainStep")
        root.addVarName("username")
        root.addStep("MainStep", [
            ['Speak', 'Hello, ', 'username', '!'],
            ['Listen', '5'],
            ['Branch']
        ])
        root.addBranch('投诉', 'ComplaintStep')
        root.addStep('ComplaintStep', [
            ['Speak', 'We are sorry for the inconvenience, ', 'username', '.'],
            ['Exit']
        ])
        
        # 初始化解释器
        interpreter = Interpreter(root)
        
        with patch.object(interpreter, 'getInput', return_value=True):
            interpreter.userInput = '投诉'
            interpreter.dispatch()
        
        # 检查用户表是否正确获取
        self.assertEqual(interpreter.userTable.getTable()['username'], 'Charlie')

if __name__ == "__main__":
    unittest.main()

import unittest
from src.Interpreter.DataStructure import Root
from src.Interpreter.Grammar import Grammar

class TestGrammar(unittest.TestCase):
    def test_process_tokens(self):
        tokens = [
            ['Step', 'MainStep'],
            ['Speak', '"Hello, World!"'],
            ['Listen', '5'],
            ['Branch', '"Option1"', 'Step1'],
            ['Silence', 'Step2'],
            ['Default', 'Step3'],
            ['Exit']
        ]
        grammar = Grammar(tokens)
        grm_tree = grammar.getGrmTree()
        
        # Check main step
        self.assertEqual(grm_tree.getMainStep(), 'MainStep')
        
        # Check if steps are correctly added
        self.assertIn('MainStep', grm_tree.getStep())
        main_step = grm_tree.getStep()['MainStep']
        self.assertEqual(len(main_step), 6)
        self.assertEqual(main_step[0], ['Speak', 'Hello, World!'])
        self.assertEqual(main_step[1], ['Listen', '5'])
        self.assertEqual(main_step[2], ['Branch'])
        self.assertEqual(main_step[3], ['Silence', 'Step2'])
        self.assertEqual(main_step[4], ['Default', 'Step3'])
        self.assertEqual(main_step[5], ['Exit'])

        # Check variable names (should be empty)
        self.assertEqual(grm_tree.getVarName(), [])

        # Check branches
        self.assertIn('Option1', grm_tree.getBranch())
        self.assertEqual(grm_tree.getBranch()['Option1'], 'Step1')


if __name__ == "__main__":
    unittest.main()

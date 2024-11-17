import unittest
from src.Interpreter.DataStructure import Root
from src.Interpreter.Grammar import Grammar

class TestGrammar(unittest.TestCase):
    def testProcessTokens(self):
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
        grmTree = grammar.getGrmTree()
        
        # Check main step
        self.assertEqual(grmTree.getMainStep(), 'MainStep')
        
        # Check if steps are correctly added
        self.assertIn('MainStep', grmTree.getStep())
        mainStep = grmTree.getStep()['MainStep']
        self.assertEqual(len(mainStep), 6)
        self.assertEqual(mainStep[0], ['Speak', 'Hello, World!'])
        self.assertEqual(mainStep[1], ['Listen', '5'])
        self.assertEqual(mainStep[2], ['Branch'])
        self.assertEqual(mainStep[3], ['Silence', 'Step2'])
        self.assertEqual(mainStep[4], ['Default', 'Step3'])
        self.assertEqual(mainStep[5], ['Exit'])

        # Check variable names (should be empty)
        self.assertEqual(grmTree.getVarName(), [])

        # Check branches
        self.assertIn('Option1', grmTree.getBranch())
        self.assertEqual(grmTree.getBranch()['Option1'], 'Step1')


if __name__ == "__main__":
    unittest.main()

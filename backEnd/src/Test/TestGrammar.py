import unittest
from src.Interpreter.Grammar import Grammar

class TestGrammar(unittest.TestCase):
    def setUp(self):
        self.tokens = [
            ['Step', 'main'],
            ['Speak', '"Hello World"'],
            ['Listen', '5'],
            ['Exit']
        ]
        self.grammar = Grammar(self.tokens)

    def testGrammarTree(self):
        grmTree = self.grammar.getGrmTree()
        # Test the main step
        self.assertEqual(grmTree.getMainStep(), 'main')
        # Test the step content
        steps = grmTree.getStep()
        self.assertIn('main', steps)
        # Remove .getStep() here
        stepContent = steps['main']
        expectedStepContent = [
            ['Speak', 'Hello World'],
            ['Listen', '5'],
            ['Exit']
        ]
        self.assertEqual(stepContent, expectedStepContent)

    def testVariableNames(self):
        tokensWithVars = [
            ['Step', 'main'],
            ['Speak', '"Hello World"'],
            ['Speak', '$name'],
            ['Exit']
        ]
        grammar = Grammar(tokensWithVars)
        grmTree = grammar.getGrmTree()
        varNames = grmTree.getVarName()
        self.assertIn('name', varNames)

    def testProcessError(self):
        tokensWithError = [
            ['Step'],
            ['Speak', 'Hello']
        ]
        # Capture error output
        from io import StringIO
        import sys
        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        grammar = Grammar(tokensWithError)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue().strip()
        self.assertIn("Error: Invalid token", output)

if __name__ == '__main__':
    unittest.main()
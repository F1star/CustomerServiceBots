# testInterpreter.py

import unittest
import threading
from src.Interpreter.DataStructure import Root, Step, Expression
from src.Interpreter.Interpreter import Interpreter
from src.Interpreter.Grammar import Grammar

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        # Define tokens for the interpreter
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
        # Capture print output
        from io import StringIO
        import sys
        capturedOutput = StringIO()
        sys.stdout = capturedOutput

        # Start interpreter in a separate thread
        threading.Thread(target=self.interpreter.dispatch).start()

        # Wait for output
        import time
        time.sleep(0.5)  # Adjusted sleep time if necessary

        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue().strip()
        self.assertIn("Hello World", output)

    def testInterpreterListenAndBranch(self):
        # Provide user input
        def provideInput():
            import time
            time.sleep(0.2)
            self.interpreter.setUserInput("yes")

        threading.Thread(target=provideInput).start()

        # Capture print output
        from io import StringIO
        import sys
        capturedOutput = StringIO()
        sys.stdout = capturedOutput

        self.interpreter.dispatch()

        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue().strip()
        self.assertIn("Hello World", output)
        self.assertIn("You said yes", output)

    def testInterpreterSilence(self):
        # Do not provide input to test silence branch
        # Capture print output
        from io import StringIO
        import sys
        capturedOutput = StringIO()
        sys.stdout = capturedOutput

        self.interpreter.dispatch()

        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue().strip()
        self.assertIn("No response received", output)

if __name__ == '__main__':
    unittest.main()
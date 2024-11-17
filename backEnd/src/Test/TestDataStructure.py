import unittest
from unittest.mock import patch
from src.Interpreter.DataStructure import Root, Step, Expression, UserTable

class TestDataStructure(unittest.TestCase):
    def testRoot(self):
        root = Root()
        root.setName("TestRoot")
        root.setMainStep("MainStep")
        root.addStep("Step1", ["Speak", "Hello"])
        root.addVarName("username")
        root.addBranch("Branch1", "Step2")
        
        self.assertEqual(root.getName(), "TestRoot")
        self.assertEqual(root.getMainStep(), "MainStep")
        self.assertIn("Step1", root.getStep())
        self.assertEqual(root.getStep()["Step1"], ["Speak", "Hello"])
        self.assertIn("username", root.getVarName())
        self.assertIn("Branch1", root.getBranch())
        self.assertEqual(root.getBranch()["Branch1"], "Step2")

    def testStep(self):
        step = Step()
        step.setStepID("Step1")
        step.addStep(["Speak", "Hello"])
        step.addStep(["Listen", "5"])
        
        self.assertEqual(step.getStepID(), "Step1")
        self.assertEqual(len(step.getStep()), 2)
        self.assertEqual(step.getStep()[0], ["Speak", "Hello"])
        self.assertEqual(step.getStep()[1], ["Listen", "5"])

    def testExpression(self):
        expr = Expression()
        expr.addExpr("Speak")
        expr.addExpr("Hello, World!")
        
        self.assertEqual(len(expr.getExpr()), 2)
        self.assertEqual(expr.getExpr()[0], "Speak")
        self.assertEqual(expr.getExpr()[1], "Hello, World!")

    @patch('builtins.input', side_effect=["Alice", "Bob"])
    def testUserTable(self, mock_input):
        userTable = UserTable(["firstName", "lastName"])
        table = userTable.getTable()
        
        self.assertEqual(table["firstName"], "Alice")
        self.assertEqual(table["lastName"], "Bob")

if __name__ == "__main__":
    unittest.main()

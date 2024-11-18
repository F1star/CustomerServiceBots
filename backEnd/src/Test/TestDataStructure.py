# testDataStructure.py

import unittest
from src.Interpreter.DataStructure import Root, Step, Expression, UserTable

class TestRoot(unittest.TestCase):
    def setUp(self):
        self.root = Root()
    
    def testInitialization(self):
        self.assertEqual(self.root.stepTable, {})
        self.assertIsNone(self.root.mainStep)
        self.assertEqual(self.root.varName, [])
        self.assertEqual(self.root.branchTable, {})
    
    def testGetStep(self):
        self.assertEqual(self.root.getStep(), {})
    
    def testSetAndGetMainStep(self):
        self.root.setMainStep('main')
        self.assertEqual(self.root.getMainStep(), 'main')
    
    def testAddStep(self):
        step = Step()
        self.root.addStep('step1', step)
        self.assertIn('step1', self.root.getStep())
        self.assertEqual(self.root.getStep()['step1'], step)
    
    def testAddVarName(self):
        self.root.addVarName('var1')
        self.assertIn('var1', self.root.getVarName())
        self.root.addVarName('var1')  # Should not duplicate
        self.assertEqual(len(self.root.getVarName()), 1)
    
    def testAddBranch(self):
        branch = 'branch_content'
        self.root.addBranch('branch1', branch)
        self.assertIn('branch1', self.root.getBranch())
        self.assertEqual(self.root.getBranch()['branch1'], branch)

class TestStep(unittest.TestCase):
    def setUp(self):
        self.step = Step()
    
    def testInitialization(self):
        self.assertIsNone(self.step.stepID)
        self.assertEqual(self.step.step, [])
    
    def testSetAndGetStepID(self):
        self.step.setStepID('step1')
        self.assertEqual(self.step.getStepID(), 'step1')
    
    def testAddStep(self):
        expr = 'expression'
        self.step.addStep(expr)
        self.assertIn(expr, self.step.getStep())

class TestExpression(unittest.TestCase):
    def setUp(self):
        self.expr = Expression()
    
    def testInitialization(self):
        self.assertEqual(self.expr.expr, [])
    
    def testAddExpr(self):
        self.expr.addExpr('expr1')
        self.assertIn('expr1', self.expr.getExpr())

class TestUserTable(unittest.TestCase):
    def setUp(self):
        self.userTable = UserTable(['var1', 'var2'])
    
    def testInitialization(self):
        self.assertEqual(self.userTable.userTable, {})
        self.assertEqual(self.userTable.varName, ['var1', 'var2'])
    
    def testSetName(self):
        self.userTable.setName('username')
        self.assertEqual(self.userTable.getTable()['name'], 'username')
    
    def testSetUser(self):
        self.userTable.setUser('age', 30)
        self.assertEqual(self.userTable.getTable()['age'], 30)
    
    def testGetTable(self):
        self.userTable.setUser('key', 'value')
        table = self.userTable.getTable()
        self.assertEqual(table['key'], 'value')

if __name__ == '__main__':
    unittest.main()

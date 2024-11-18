import unittest
from src.Interpreter.DataStructure import Root, Step, Expression, UserTable

class TestRoot(unittest.TestCase):
    """
    测试Root类的功能
    """
    def setUp(self):
        """每个测试之前初始化Root实例"""
        self.root = Root()
    
    def testInitialization(self):
        """测试Root类初始化后的默认值"""
        self.assertEqual(self.root.stepTable, {})  # stepTable 应为空字典
        self.assertIsNone(self.root.mainStep)  # mainStep 应为None
        self.assertEqual(self.root.varName, [])  # varName 应为空列表
        self.assertEqual(self.root.branchTable, {})  # branchTable 应为空字典
    
    def testGetStep(self):
        """测试getStep方法"""
        self.assertEqual(self.root.getStep(), {})  # 初始返回空字典
    
    def testSetAndGetMainStep(self):
        """测试setMainStep和getMainStep方法"""
        self.root.setMainStep('main')  # 设置 mainStep
        self.assertEqual(self.root.getMainStep(), 'main')  # 获取 mainStep 应为 'main'
    
    def testAddStep(self):
        """测试addStep方法"""
        step = Step()  # 创建一个Step对象
        self.root.addStep('step1', step)  # 添加step到stepTable中
        self.assertIn('step1', self.root.getStep())  # step1 应在stepTable中
        self.assertEqual(self.root.getStep()['step1'], step)  # step1对应的值应为step对象
    
    def testAddVarName(self):
        """测试addVarName方法"""
        self.root.addVarName('var1')  # 添加 var1
        self.assertIn('var1', self.root.getVarName())  # var1 应在 varName 列表中
        self.root.addVarName('var1')  # 不应该重复添加
        self.assertEqual(len(self.root.getVarName()), 1)  # varName 列表的长度应为 1
    
    def testAddBranch(self):
        """测试addBranch方法"""
        branch = 'branch_content'  # 假设一个分支内容
        self.root.addBranch('branch1', branch)  # 添加分支到branchTable中
        self.assertIn('branch1', self.root.getBranch())  # branch1 应在 branchTable 中
        self.assertEqual(self.root.getBranch()['branch1'], branch)  # branch1 对应的值应为 branch

class TestStep(unittest.TestCase):
    """
    测试Step类的功能
    """
    def setUp(self):
        """每个测试之前初始化Step实例"""
        self.step = Step()
    
    def testInitialization(self):
        """测试Step类初始化后的默认值"""
        self.assertIsNone(self.step.stepID)  # stepID 应为 None
        self.assertEqual(self.step.step, [])  # step 列表应为空
    
    def testSetAndGetStepID(self):
        """测试setStepID和getStepID方法"""
        self.step.setStepID('step1')  # 设置 stepID
        self.assertEqual(self.step.getStepID(), 'step1')  # 获取 stepID 应为 'step1'
    
    def testAddStep(self):
        """测试addStep方法"""
        expr = 'expression'  # 假设一个表达式
        self.step.addStep(expr)  # 添加表达式到step中
        self.assertIn(expr, self.step.getStep())  # 表达式应在 step 列表中

class TestExpression(unittest.TestCase):
    """
    测试Expression类的功能
    """
    def setUp(self):
        """每个测试之前初始化Expression实例"""
        self.expr = Expression()
    
    def testInitialization(self):
        """测试Expression类初始化后的默认值"""
        self.assertEqual(self.expr.expr, [])  # expr 应为空列表
    
    def testAddExpr(self):
        """测试addExpr方法"""
        self.expr.addExpr('expr1')  # 添加表达式
        self.assertIn('expr1', self.expr.getExpr())  # expr1 应在 expr 列表中

class TestUserTable(unittest.TestCase):
    """
    测试UserTable类的功能
    """
    def setUp(self):
        """每个测试之前初始化UserTable实例"""
        self.userTable = UserTable(['var1', 'var2'])  # 假设初始化时传入 varName 列表
    
    def testInitialization(self):
        """测试UserTable初始化后的默认值"""
        self.assertEqual(self.userTable.userTable, {})  # userTable 应为空字典
        self.assertEqual(self.userTable.varName, ['var1', 'var2'])  # varName 应为 ['var1', 'var2']
    
    def testSetName(self):
        """测试setName方法"""
        self.userTable.setName('username')  # 设置用户名字
        self.assertEqual(self.userTable.getTable()['name'], 'username')  # 获取用户表中的 name 应为 'username'
    
    def testSetUser(self):
        """测试setUser方法"""
        self.userTable.setUser('age', 30)  # 设置用户年龄
        self.assertEqual(self.userTable.getTable()['age'], 30)  # 获取用户表中的 age 应为 30
    
    def testGetTable(self):
        """测试getTable方法"""
        self.userTable.setUser('key', 'value')  # 添加一个键值对
        table = self.userTable.getTable()  # 获取整个表
        self.assertEqual(table['key'], 'value')  # 表中的 key 应对应 value

if __name__ == '__main__':
    unittest.main()  # 运行测试

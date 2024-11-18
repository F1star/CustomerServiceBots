import unittest
from src.Interpreter.app import app, userInfo, userState

class TestApp(unittest.TestCase):
    """
    该测试确保应用的各个API接口按预期工作。
    """

    def setUp(self):
        """
        设置测试环境，启用Flask测试模式，并创建测试客户端。
        """
        app.config['TESTING'] = True
        self.client = app.test_client()
        # 清空用户信息和状态
        userInfo.clear()
        userState.clear()

    def testRegisterAndLogin(self):
        """
        测试用户注册和登录功能。
        """
        # 注册用户
        response = self.client.post('/register', data={'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data['message'], '注册成功')

        # 重复注册，应该返回错误
        response = self.client.post('/register', data={'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertEqual(response_data.get('error'), '用户名已存在')

        # 使用正确的凭证登录
        response = self.client.post('/login', data={'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data['message'], '登录成功')

        # 使用错误的凭证登录
        response = self.client.post('/login', data={'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)
        response_data = response.get_json()
        self.assertEqual(response_data.get('error'), '凭证无效')

    def testGetAndSetInfo(self):
        """
        测试获取和设置用户信息的功能。
        """
        # 注册并登录
        self.client.post('/register', data={'username': 'testuser', 'password': 'password'})
        self.client.post('/login', data={'username': 'testuser', 'password': 'password'})

        # 设置信息
        response = self.client.post('/setinfo', data={'username': 'testuser', 'name': 'Alice', 'amount': '100'})
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data['message'], '信息设置成功')

        # 获取信息
        response = self.client.post('/getinfo', data={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)
        actual_vars = response.get_json()
        expected_vars = ['name', 'amount']  # 确保返回的字段与设置的一致
        self.assertEqual(actual_vars, expected_vars)

    def testChatFlow(self):
        """
        测试完整的聊天流程。
        """
        # 注册并登录
        self.client.post('/register', data={'username': 'testuser', 'password': 'password'})
        self.client.post('/login', data={'username': 'testuser', 'password': 'password'})

        # 清除聊天记录
        response = self.client.post('/clearchat', data={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)

        # 获取初始聊天记录（应该为空）
        response = self.client.post('/repeatchat', data={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)

        # 用户输入"账单"
        response = self.client.post('/telechat', data={'username': 'testuser', 'message': '账单'})
        self.assertEqual(response.status_code, 200)

        # 获取机器人的回复
        response = self.client.post('/repeatchat', data={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()  # 执行测试

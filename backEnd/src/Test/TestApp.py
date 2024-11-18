import unittest
from src.Interpreter.app import app, userInfo, userState

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        # 清空用户信息和状态
        userInfo.clear()
        userState.clear()

    def testRegisterAndLogin(self):
        # 注册用户
        response = self.client.post('/register', data={'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data['message'], '注册成功')

        # 重复注册
        response = self.client.post('/register', data={'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 400)
        response_data = response.get_json()
        self.assertEqual(response_data.get('error'), '用户名已存在')

        # 正确登录
        response = self.client.post('/login', data={'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data['message'], '登录成功')

        # 错误登录
        response = self.client.post('/login', data={'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)
        response_data = response.get_json()
        self.assertEqual(response_data.get('error'), '凭证无效')

    def testGetAndSetInfo(self):
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
        expected_vars = ['name', 'amount'] 
        self.assertEqual(actual_vars, expected_vars)

    def testChatFlow(self):
        # 注册并登录
        self.client.post('/register', data={'username': 'testuser', 'password': 'password'})
        self.client.post('/login', data={'username': 'testuser', 'password': 'password'})

        # 清除聊天记录
        response = self.client.post('/clearchat', data={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)

        # 获取机器人回复
        response = self.client.post('/repeatchat', data={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)

        # 发送用户输入
        response = self.client.post('/telechat', data={'username': 'testuser', 'message': '账单'})
        self.assertEqual(response.status_code, 200)

        # 获取机器人回复
        response = self.client.post('/repeatchat', data={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

import threading
from threading import Lock
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.Interpreter.Lexical import Lexical
from src.Interpreter.Grammar import Grammar
from src.Interpreter.Interpreter import Interpreter

app = Flask(__name__)
CORS(app)  # 启用跨域请求

# 初始化解释器基础实例
lex = Lexical('src/Test/Example/test1.txt')  # 词法分析器实例，读取文件并解析
lex.printTokens()  # 打印解析出的词法单元
grmTree = Grammar(lex.getTokens())  # 使用解析出的tokens创建语法树
print(grmTree.getGrmTree().getStep())  # 打印语法树步骤
print(grmTree.getGrmTree().getVarName())  # 打印语法树变量名
print(grmTree.getGrmTree().getBranch())  # 打印语法树分支

# 用户信息存储（临时内存）
userInfo = {}
userInfoLock = Lock()  # 用于锁定用户信息字典

userState = {}
userStateLock = Lock()  # 用于锁定用户状态字典

def runDispatch(username):
    """
    启动用户的解释器调度
    """
    userState[username].dispatch()  # 执行用户的调度逻辑
    return

@app.route('/register', methods=['POST'])
def register():
    """
    用户注册，接收用户名和密码。
    """
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': '用户名和密码是必需的'}), 400  # 必填字段检查

    with userInfoLock:
        if username in userInfo:
            return jsonify({'error': '用户名已存在'}), 400  # 用户已存在检查
        userInfo[username] = password  # 存储用户信息

    return jsonify({'message': '注册成功'}), 200

@app.route('/login', methods=['POST'])
def login():
    """
    用户登录，验证用户名和密码。
    """
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': '用户名和密码是必需的'}), 400  # 必填字段检查

    with userInfoLock:
        if username not in userInfo:
            return jsonify({'error': '用户名不存在'}), 404  # 用户不存在检查
        if userInfo[username] != password:
            return jsonify({'error': '凭证无效'}), 401  # 密码不匹配检查

    interpreter = Interpreter(grmTree.getGrmTree())  # 初始化解释器
    interpreter.setName(username)  # 设置用户名

    with userStateLock:
        userState[username] = interpreter  # 存储用户状态

    return jsonify({'message': '登录成功'}), 200

@app.route('/getinfo', methods=['POST'])
def getInfo():
    """
    获取用户信息。
    """
    username = request.form.get('username')
    with userStateLock:
        if username not in userState:
            return jsonify({'error': '用户未登录'}), 403  # 检查用户是否登录
        result = userState[username].getInfo()  # 获取用户的变量信息
    return jsonify(result), 200

@app.route('/setinfo', methods=['POST'])
def setInfo():
    """
    设置用户信息。
    """
    username = request.form.get('username')
    with userStateLock:
        if username not in userState:
            return jsonify({'error': '用户未登录'}), 403  # 检查用户是否登录
        # 更新用户信息
        for infoName in userState[username].getInfo():
            userInfoValue = request.form.get(infoName)
            userState[username].setInfo(infoName, userInfoValue)  # 设置用户信息
            print(infoName, userInfoValue)
    return jsonify({'message': '信息设置成功'}), 200

@app.route('/clearchat', methods=['POST'])
def clearChat():
    """
    清除当前对话并启动新线程执行调度。
    """
    username = request.form.get('username')
    print(username)
    with userStateLock:
        if username not in userState:
            return jsonify({'error': '用户未登录'}), 403  # 检查用户是否登录
        # 创建一个后台线程来执行 dispatch() 方法
        thread = threading.Thread(target=runDispatch, args=(username,))
        thread.start()  # 启动线程

    return jsonify({'message': '对话已清除'}), 200

@app.route('/telechat', methods=['POST'])
def chat():
    """
    接收用户输入并传递给解释器。
    """
    username = request.form.get('username')
    userInput = request.form.get('message')

    with userStateLock:
        if username not in userState:
            return jsonify({'error': '用户未登录'}), 403  # 检查用户是否登录
        interpreter = userState[username]

    interpreter.setUserInput(userInput)  # 将用户输入传递给解释器
    return jsonify({'message': '输入已接收'}), 200

@app.route('/repeatchat', methods=['POST'])
def repeatChat():
    """
    获取并返回最新的解释结果。
    """
    username = request.form.get('username')
    with userStateLock:
        if username not in userState:
            return jsonify({'error': '用户未登录'}), 403  # 检查用户是否登录
        interpreter = userState[username]

    result = interpreter.getLatestResult()  # 获取最新的解释结果
    if result:
        return jsonify({'message': result}), 200
    else:
        return jsonify({'message': '没有新消息'}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)  # 启动Flask应用，调试模式，端口5000

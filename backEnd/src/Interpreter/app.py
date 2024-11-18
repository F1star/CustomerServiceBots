import threading
from threading import Lock
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.Interpreter.Lexical import Lexical
from src.Interpreter.Grammar import Grammar
from src.Interpreter.Interpreter import Interpreter

app = Flask(__name__)
CORS(app)

# 初始化解释器的基础实例
lex = Lexical('src/Test/Example/test1.txt')
lex.printTokens()
grmTree = Grammar(lex.getTokens())
print(grmTree.getGrmTree().getStep())
print(grmTree.getGrmTree().getVarName())
print(grmTree.getGrmTree().getBranch())

# 用户状态存储（临时内存中）
userInfo = {}
userInfoLock = Lock()

userState = {}
userStateLock = Lock()

def runDispatch(username):
    userState[username].dispatch()
    return

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': '用户名和密码是必需的'}), 400

    with userInfoLock:
        if username in userInfo:
            return jsonify({'error': '用户名已存在'}), 400
        userInfo[username] = password

    return jsonify({'message': '注册成功'}), 200


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': '用户名和密码是必需的'}), 400

    with userInfoLock:
        if username not in userInfo:
            return jsonify({'error': '用户名不存在'}), 404
        if userInfo[username] != password:
            return jsonify({'error': '凭证无效'}), 401

    interpreter = Interpreter(grmTree.getGrmTree())
    interpreter.setName(username)

    with userStateLock:
        userState[username] = interpreter

    return jsonify({'message': '登录成功'}), 200

@app.route('/getinfo', methods=['POST'])
def getInfo():
    username = request.form.get('username')
    with userStateLock:
        if username not in userState:
            return jsonify({'error': '用户未登录'}), 403
        result = userState[username].getInfo()
    return jsonify(result), 200

@app.route('/setinfo', methods=['POST'])
def setInfo():
    username = request.form.get('username')
    with userStateLock:
        if username not in userState:
            return jsonify({'error': '用户未登录'}), 403
        for infoName in userState[username].getInfo():
            userInfoValue = request.form.get(infoName)
            userState[username].setInfo(infoName, userInfoValue)
            print(infoName, userInfoValue)
    return jsonify({'message': '信息设置成功'}), 200

@app.route('/clearchat', methods=['POST'])
def clearChat():
    username = request.form.get('username')
    print(username)
    with userStateLock:
        if username not in userState:
            return jsonify({'error': '用户未登录'}), 403
        # 创建一个后台线程来执行 dispatch() 方法
        thread = threading.Thread(target=runDispatch, args=(username,))
        thread.start()
    return jsonify({'message': '对话已清除'}), 200

@app.route('/telechat', methods=['POST'])
def chat():
    username = request.form.get('username')
    userInput = request.form.get('message')

    with userStateLock:
        if username not in userState:
            return jsonify({'error': '用户未登录'}), 403
        interpreter = userState[username]

    interpreter.setUserInput(userInput)
    return jsonify({'message': '输入已接收'}), 200

@app.route('/repeatchat', methods=['POST'])
def repeatChat():
    username = request.form.get('username')
    with userStateLock:
        if username not in userState:
            return jsonify({'error': '用户未登录'}), 403
        interpreter = userState[username]

    result = interpreter.getLatestResult()
    if result:
        return jsonify({'message': result}), 200
    else:
        return jsonify({'message': '没有新消息'}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)

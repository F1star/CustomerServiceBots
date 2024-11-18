# CustomerServiceBots
## 作业描述：
领域特定语言（Domain Specific Language，DSL）可以提供一种相对简单的文法，用于特定领域的业务流程定制。本作业要求定义一个领域特定脚本语言，这个语言能够描述在线客服机器人（机器人客服是目前提升客服效率的重要技术，在银行、通信和商务等领域的复杂信息系统中有广泛的应用）的自动应答逻辑，并设计实现一个解释器解释执行这个脚本，可以根据用户的不同输入，根据脚本的逻辑设计给出相应的应答。

## 基本要求：
脚本语言的语法可以自由定义，只要语义上满足描述客服机器人自动应答逻辑的要求。

程序输入输出形式不限，可以简化为纯命令行界面。

应该给出几种不同的脚本范例，对不同脚本范例解释器执行之后会有不同的行为表现。

## 评分标准：
本作业考察学生规范编写代码、合理设计程序、解决工程问题等方面的综合能力。满分100分，具体如下：

风格：满分15分，其中代码注释6分，命名6分，其它3分。

设计和实现：满分30分，其中数据结构7分，模块划分7分，功能8分，文档8分。

接口：满分15分，其中程序间接口8分，人机接口7分。

测试：满分30分，测试桩15分，自动测试脚本15分

记法：满分10分，文档中对此脚本语言的语法的准确描述。

## 提交文件：
报告
程序源代码
可执行文件

```python
# Modified Python Flask application

import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.Interpreter.Lexical import Lexical
from src.Interpreter.Grammar import Grammar
from src.Interpreter.Interpreter import Interpreter

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Initialize the base interpreter instance
lex = Lexical('src/Test/Example/test1.txt')
lex.printTokens()
grmTree = Grammar(lex.getTokens())

# User state storage (in temporary memory)
userInfo = {}  # Stores usernames and passwords
userState = {}  # Stores interpreter instances for logged-in users

def runDispatch(username):
    userState[username].dispatch()
    return

@app.route('/register', methods=['POST'])
async def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if username in userInfo:
        return jsonify({'error': 'Username already exists'}), 400

    userInfo[username] = password
    return jsonify({'message': 'Register successful'}), 200

@app.route('/login', methods=['POST'])
async def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if username not in userInfo:
        return jsonify({'error': 'Username does not exist'}), 404

    if userInfo[username] == password:
        userState[username] = Interpreter(grmTree.getGrmTree())
        interpreter = userState[username]
        interpreter.setName(username)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/getinfo', methods=['POST'])
async def getInfo():
    username = request.form.get('username')
    result = userState[username].getInfo()
    return jsonify(result), 200

@app.route('/setinfo', methods=['POST'])
async def setInfo():
    username = request.form.get('username')
    for infoName in userState[username].getInfo():
        userInfoValue = request.form.get(infoName)
        userState[username].setInfo(infoName, userInfoValue)
        print(infoName, userInfoValue)
    return jsonify({'message': 'Set info successful'}), 200

@app.route('/clearchat', methods=['POST'])
async def clearChat():
    username = request.form.get('username')
    print(username)
    # Create a background thread to execute the dispatch() method
    thread = threading.Thread(target=runDispatch, args=(username,))
    thread.start()
    return jsonify({'message': 'Chat cleared'}), 200

@app.route('/telechat', methods=['POST'])
async def chat():
    username = request.form.get('username')
    userInput = request.form.get('message')

    if username not in userState:
        return jsonify({'error': 'User not logged in'}), 403

    userState[username].userInput = userInput
    while True:
        if userState[username].isFlag:
            runflag = userState[username].runFlag - 1
            result = userState[username].runStack[runflag]
            userState[username].isFlag = False
            print(result)
            return jsonify(result), 200

@app.route('/repeatchat', methods=['POST'])
async def repeatChat():
    username = request.form.get('username')
    if username not in userState:
        return jsonify({'error': 'User not logged in'}), 403

    if userState[username].isFlag and userState[username].userInput is None:
        runflag = userState[username].runFlag - 1
        result = userState[username].runStack[runflag]
        userState[username].isFlag = False
        print(result)
        return jsonify(result), 200
    else:
        return jsonify({'message': 'No new messages'}), 204

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

```vue
<!-- Modified Vue.js component -->

<template>
    <div style="width: 100%; height: 100%; padding: 16px; border: 1px solid #f0f0f0; border-radius: 4px;">
        <a-card title="Multi-turn Dialogue">
            <a-button type="primary" ghost @click="clearChat">New Chat</a-button>
            <div class="chat-messages">
                <div v-for="(message, index) in messages" :key="index" class="chat-message">
                    <a-comment>
                        <template #actions>
                            <span key="comment-basic-like">
                                <a-tooltip title="Like">
                                    <template v-if="message.action === 'liked'">
                                        <LikeFilled @click="like(index)" />
                                    </template>
                                    <template v-else>
                                        <LikeOutlined @click="like(index)" />
                                    </template>
                                </a-tooltip>
                                <span style="padding-left: 8px; cursor: auto">
                                    {{ message.likes }}
                                </span>
                            </span>
                            <span key="comment-basic-dislike">
                                <a-tooltip title="Dislike">
                                    <template v-if="message.action === 'disliked'">
                                        <DislikeFilled @click="dislike(index)" />
                                    </template>
                                    <template v-else>
                                        <DislikeOutlined @click="dislike(index)" />
                                    </template>
                                </a-tooltip>
                                <span style="padding-left: 8px; cursor: auto">
                                    {{ message.dislikes }}
                                </span>
                            </span>
                            <span key="comment-basic-reply-to">Reply to</span>
                        </template>
                        <template #author><a>{{ message.role }}</a></template>
                        <template #avatar>
                            <a-avatar v-if="message.role==='Assistant'" src="../../image/teleBot.png" alt="Assistant" />
                            <a-avatar v-if="message.role==='User'" src="../../image/User.png" alt="User" />
                        </template>
                        <template #content>
                            <div class="markdown-body" v-html="md.render(message.content)"></div>
                        </template>
                        <template #datetime>
                            <a-tooltip :title="message.timestamp.format('YYYY-MM-DD HH:mm:ss')">
                                <span>{{ message.timestamp.fromNow() }}</span>
                            </a-tooltip>
                        </template>
                    </a-comment>
                </div>
                <a-spin v-if="loading" class="loading-spinner">
                    <div class="chat-message"><strong>Loading...</strong></div>
                </a-spin>
            </div>
            <div class="chat-input">
                <a-textarea v-model:value="input" @keyup.enter="sendMessage" placeholder="Type a message..."
                    :auto-size="{ minRows: 5, maxRows: 10 }" />
                <a-button @click="sendMessage" type="primary" style="margin-top: 10px;">Send</a-button>
            </div>
        </a-card>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useTeleChatStore } from '../apis/Chat/chatStore';
import { mainStore } from '../store';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import markdownIt from 'markdown-it';
import hljs from 'highlight.js';
import { LikeOutlined, LikeFilled, DislikeOutlined, DislikeFilled } from '@ant-design/icons-vue';

export default {
    components: {
        LikeOutlined,
        LikeFilled,
        DislikeOutlined,
        DislikeFilled,
    },
    setup() {
        dayjs.extend(relativeTime);
        const messages = ref([]);
        const input = ref('');
        const loading = ref(false);
        const chatStore = useTeleChatStore();
        const userStore = mainStore();
        const md = new markdownIt({
            highlight: function (str, lang) {
                if (lang && hljs.getLanguage(lang)) {
                    try {
                        return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang }).value}</code></pre>`;
                    } catch (__) {}
                }
                return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
            }
        });

        const like = (index) => {
            const message = messages.value[index];
            message.likes = 1;
            message.dislikes = 0;
            message.action = 'liked';
        };

        const dislike = (index) => {
            const message = messages.value[index];
            message.likes = 0;
            message.dislikes = 1;
            message.action = 'disliked';
        };

        const clearChat = async () => {
            try {
                const formData = new FormData();
                formData.append('username', userStore.username);
                const res = await chatStore.clearChat(formData);
                if (res.status === 200) {
                    messages.value = [];
                    pollMessages();
                }
            } catch (error) {
                console.error('Error clearing chat:', error);
            }
        };

        const sendMessage = async () => {
            if (input.value.trim() === '') return;

            const newMessage = {
                role: 'User',
                content: input.value,
                likes: 0,
                dislikes: 0,
                action: null,
                timestamp: dayjs(),
            };

            messages.value.push(newMessage);
            loading.value = true;
            const formData = new FormData();
            formData.append('username', userStore.username);
            formData.append('message', input.value);
            input.value = '';
            try {
                const response = await chatStore.teleChat(formData);
                if (response.status === 200) {
                    messages.value.push({
                        role: 'Assistant',
                        content: response.data,
                        likes: 0,
                        dislikes: 0,
                        action: null,
                        timestamp: dayjs(),
                    });
                }
            } catch (error) {
                console.error('Error sending message:', error);
                messages.value.push({
                    role: 'Assistant',
                    content: 'Error sending message.',
                    likes: 0,
                    dislikes: 0,
                    action: null,
                    timestamp: dayjs(),
                });
            } finally {
                loading.value = false;
            }
        };

        const pollMessages = () => {
            setInterval(async () => {
                const formData = new FormData();
                formData.append('username', userStore.username);
                try {
                    const res = await chatStore.repeatChat(formData);
                    if (res.status === 200) {
                        messages.value.push({
                            role: 'Assistant',
                            content: res.data,
                            likes: 0,
                            dislikes: 0,
                            action: null,
                            timestamp: dayjs(),
                        });
                    }
                } catch (error) {
                    console.error('Error polling messages:', error);
                }
            }, 3000); // Poll every 3 seconds
        };

        onMounted(() => {
            clearChat();
        });

        return {
            messages,
            input,
            sendMessage,
            loading,
            like,
            dislike,
            dayjs,
            md,
            clearChat,
        };
    },
};
</script>

<style scoped>
.chat-input {
    margin-bottom: 10px;
    display: flex;
    flex-direction: column;
}

.chat-messages {
    flex-grow: 1;
    overflow-y: auto;
}

.chat-message {
    margin-bottom: 10px;
}

.markdown-body {
    font-size: 16px;
}
</style>

```

```python
# Modified Interpreter class

import threading
import time
from src.Interpreter.DataStructure import UserTable

class Interpreter:
    def __init__(self, tree):
        """
        Initialize the interpreter with the syntax tree.
        """
        self.tree = tree
        self.userTable = UserTable(tree.getVarName())
        self.mainStep = tree.getMainStep()
        self.curStep = None
        self.userInput = None
        self.runStack = []
        self.runFlag = 0
        self.isFlag = False
        self.input_event = threading.Event()

    def setName(self, name):
        self.userTable.setName(name)

    def setInfo(self, InfoName, userInfo):
        self.userTable.setUser(InfoName, userInfo)

    def getInfo(self):
        return self.tree.getVarName()

    def dispatch(self):
        """
        Execute steps based on the syntax tree.
        """
        stepName = self.mainStep
        isInTime = False
        while stepName:
            self.curStep = self.tree.getStep()[stepName]
            flag = False

            for state in self.curStep:
                if state[0] == 'Speak':
                    print(1)
                    self.doSpeak(state)
                elif state[0] == 'Listen':
                    print(2)
                    isInTime = self.doListen(state)
                elif state[0] == 'Branch':
                    print(3)
                    if isInTime:
                        if self.tree.getBranch().get(str(self.userInput)) is not None:
                            stepName = self.tree.getBranch()[str(self.userInput)]
                            break
                        else:
                            flag = True
                    else:
                        continue
                elif state[0] == 'Silence':
                    print(4)
                    if flag:
                        flag = False
                        continue
                    stepName = state[1]
                    break
                elif state[0] == 'Default':
                    print(5)
                    stepName = state[1]
                    break
                elif state[0] == 'Exit':
                    print(6)
                    return


    def doSpeak(self, state):
        """
        Handle the Speak instruction.
        """
        expression = ''
        for i in range(1, len(state)):
            if state[i] in self.tree.getVarName():
                expression += self.userTable.getTable()[state[i]]
            else:
                expression += state[i]
        print(expression)
        self.runStack.append(expression)
        self.runFlag += 1
        self.isFlag = True
        # Wait until the message is consumed
        while self.isFlag:
            time.sleep(0.1)
        return

    def doListen(self, state):
        """
        Handle the Listen instruction.
        """
        self.userInput = None
        isInTime = self.getInput(int(state[1]))
        return isInTime

    def getInput(self, timeout):
        """
        Wait for user input within a timeout.
        """
        self.input_event.clear()
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.userInput is not None:
                print(f"User input: {self.userInput}")
                return True
            time.sleep(0.1)

        print("Input timed out")
        return False


```
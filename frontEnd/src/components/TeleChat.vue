<template>
    <div style="width: 100%; height: 100%; padding: 16px; border: 1px solid #f0f0f0; border-radius: 4px;">
        <a-card title="多轮对话">
            <a-button type="primary" ghost @click="clearChat">新建对话</a-button>
            <div class="chat-messages">
                <div v-for="(message, index) in messages" :key="index" class="chat-message">
                    <a-comment>
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
                    <div class="chat-message"><strong>加载中...</strong></div>
                </a-spin>
            </div>
            <div class="chat-input">
                <a-textarea v-model:value="input" @keyup.enter="sendMessage" placeholder="请输入消息..."
                    :auto-size="{ minRows: 5, maxRows: 10 }" />
                <a-button @click="sendMessage" type="primary" style="margin-top: 10px;">发送</a-button>
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

export default {
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

        let pollInterval = null;

        const clearChat = async () => {
            try {
                const formData = new FormData();
                formData.append('username', userStore.username);
                const res = await chatStore.clearChat(formData);
                if (res.status === 200) {
                    messages.value = [];
                    startPolling();
                }
            } catch (error) {
                console.error('清除对话时出错:', error);
            }
        };

        const sendMessage = async () => {
            if (input.value.trim() === '') return;

            const newMessage = {
                role: 'User',
                content: input.value,
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
                    // 等待轮询函数获取机器人的回复
                }
            } catch (error) {
                console.error('发送消息时出错:', error);
                messages.value.push({
                    role: 'Assistant',
                    content: '发送消息时出错。',
                    timestamp: dayjs(),
                });
            } finally {
                loading.value = false;
            }
        };

        const pollMessages = async () => {
            const formData = new FormData();
            formData.append('username', userStore.username);
            try {
                const res = await chatStore.repeatChat(formData);
                if (res.status === 200 && res.data.message !== '没有新消息') {
                    messages.value.push({
                        role: 'Assistant',
                        content: res.data.message,
                        timestamp: dayjs(),
                    });
                }
            } catch (error) {
                console.error('轮询消息时出错:', error);
            }
        };

        const startPolling = () => {
            if (pollInterval) clearInterval(pollInterval);
            pollInterval = setInterval(pollMessages, 3000); // 每3秒轮询一次
        };

        onMounted(() => {
            clearChat();
        });

        return {
            messages,
            input,
            sendMessage,
            loading,
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

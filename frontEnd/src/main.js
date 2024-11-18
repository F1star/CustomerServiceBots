import { createApp } from 'vue';
import { createPinia } from 'pinia'
import App from './App.vue';
import Antd from 'ant-design-vue';
import router from './router'
import 'ant-design-vue/dist/reset.css';  // 引入 Ant Design 样式

const app = createApp(App);

app.use(createPinia())
app.use(router)
app.use(Antd);

app.mount('#app');
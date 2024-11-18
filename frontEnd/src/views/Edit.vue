<template>
    <a-layout style="min-height: 100vh">
      <a-layout-sider v-model:collapsed="collapsed" collapsible>
        <div class="logo" />
        <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
          <a-menu-item key="1" @click="showChat">
            <pie-chart-outlined />
            <span>信息设置</span>
          </a-menu-item>
          <a-menu-item key="2" @click="showTeleChat">
            <desktop-outlined />
            <span>智能对话</span>
          </a-menu-item>
        </a-menu>
      </a-layout-sider>
      <a-layout>
        <a-layout-header style="background: #fff; padding: 0" />
        <a-layout-content style="margin: 0 16px">
          <div v-if="activeComponent === 'info'" class="component-content">
            <a-breadcrumb style="margin: 16px 0">
              <a-breadcrumb-item>User</a-breadcrumb-item>
              <a-breadcrumb-item>{{ userStore.username }}</a-breadcrumb-item>
            </a-breadcrumb>
            <Chat />
          </div>
          <div v-if="activeComponent === 'teleChat'" class="component-content">
            <a-breadcrumb style="margin: 16px 0">
              <a-breadcrumb-item>User</a-breadcrumb-item>
              <a-breadcrumb-item>{{ userStore.username }}</a-breadcrumb-item>
            </a-breadcrumb>
            <TeleChat />
          </div>
        </a-layout-content>
        <a-layout-footer style="text-align: center">
          Custom Service Bots ©2024 Created by Li Yuxing
        </a-layout-footer>
      </a-layout>
    </a-layout>
</template>

<script setup>
  import { ref } from 'vue';
  import Chat from '../components/InfoSet.vue';
  import TeleChat from '../components/TeleChat.vue';
  import { PieChartOutlined, DesktopOutlined } from '@ant-design/icons-vue';
  import { mainStore } from '../store';

  const userStore = mainStore();
  const collapsed = ref(false);
  const selectedKeys = ref(['1']);
  const activeComponent = ref('');
  const text = ref('');
  
  const showChat = () => {
    activeComponent.value = 'info';
  }

  const showTeleChat = () => {
    activeComponent.value = 'teleChat';
  }

</script>

<style scoped>
#components-layout-demo-side .logo {
  height: 32px;
  margin: 16px;
  background: rgba(255, 255, 255, 0.3);
}

.site-layout .site-layout-background {
  background: #fff;
}
[data-theme='dark'] .site-layout .site-layout-background {
  background: #141414;
}
</style>
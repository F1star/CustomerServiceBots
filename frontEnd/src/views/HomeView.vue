<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLogin = () => {
  router.push({ name: 'login' })
}
const goToRegister = () => {
  router.push({ name: 'register' })
}
</script>

<template>
  <div class="container">
    <a-card class="box-card" hoverable>
      <template #title>
        <h2>客服机器人交互界面</h2>
      </template>
      <a-button type="primary" @click="goToLogin" class="button">登录</a-button>
      <a-button type="primary" @click="goToRegister" class="button">注册</a-button>
    </a-card>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.box-card {
  width: 300px;
}

.button {
  margin-top: 10px;
  width: 100%;
}
</style>
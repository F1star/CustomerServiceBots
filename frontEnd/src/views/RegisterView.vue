<script>
import { ref } from 'vue';
import { useUserStore } from '../apis/LoginSystem/userStore';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue';

export default {
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const user = useUserStore()

    const username = ref('')
    const password = ref('')

    const register = async () => {
      try {
        const res = await user.register({
          username: username.value,
          password: password.value
        })
        console.log("register res", res)
        if (res.status === 200) {
          message.success('Register successful!\nPlease login.')
          router.push({ name: 'login' })
        }else{
          message.error('Register failed. Please try another username.')
        }
      } catch (error) {
        message.error('Register failed. Please try another username.')
      }
    }
    return {
      username,
      password,
      register
    }
  }
}


</script>

<template>
  <main style="display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f0f2f5;">
    <a-card class="box-card" style="width: 400px;">
      <h2 style="text-align: center; margin-bottom: 20px;">注册</h2>
      <a-form>
        <a-form-item>
          <a-input v-model:value="username" placeholder="用户名"></a-input>
        </a-form-item>
        <a-form-item>
          <a-input v-model:value="password" type="password" placeholder="密码"></a-input>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="register" style="width: 100%;">注册</a-button>
        </a-form-item>
      </a-form>
    </a-card>
  </main>
</template>

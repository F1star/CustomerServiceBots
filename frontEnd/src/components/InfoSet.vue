<template>
  <a-form :layout="formState.layout" :model="formState" v-bind="formItemLayout">
    <a-form-item label="Form Layout">
      <a-radio-group v-model:value="formState.layout">
        <a-radio-button value="horizontal">Horizontal</a-radio-button>
        <a-radio-button value="vertical">Vertical</a-radio-button>
        <a-radio-button value="inline">Inline</a-radio-button>
      </a-radio-group>
    </a-form-item>

    <!-- 动态渲染表单项 -->
    <a-form-item
      v-for="(item, index) in dynamicFields"
      :key="index"
      :label="item"
    >
      <!-- 每个字段动态选择对应类型 (input 或 select)，这里假设都是 input -->
      <a-input v-model:value="formState[item]" :placeholder="`Enter ${item}`" />
    </a-form-item>

    <a-form-item :wrapper-col="buttonItemLayout.wrapperCol">
      <a-button type="primary" @click="handleSubmit">Submit</a-button>
    </a-form-item>
  </a-form>
</template>

<script setup>
import { computed, reactive, onMounted } from 'vue';
import { useGetInfoStore, useSetInfoStore } from '../apis/Info/infoStore';
import { mainStore } from '../store/index';
import { message } from 'ant-design-vue';

const getInfoStore = useGetInfoStore();
const setInfoStore = useSetInfoStore();
const userStore = mainStore();

const formState = reactive({
  layout: 'horizontal',
  // 动态字段会添加到这里
});

const dynamicFields = reactive([]); // 存储从 getInfo 获取的字段列表

const formItemLayout = computed(() => {
  const { layout } = formState;
  return layout === 'horizontal'
      ? {
          labelCol: { span: 4 },
          wrapperCol: { span: 14 },
      }
      : {};
});

const buttonItemLayout = computed(() => {
  const { layout } = formState;
  return layout === 'horizontal'
      ? {
          wrapperCol: { span: 14, offset: 4 },
      }
      : {};
});

// 获取信息，动态设置表单字段
const getInfo = async () => {
  const formData = new FormData();
  formData.append('username', userStore.username);
  const res = await getInfoStore.getInfo(formData);
  const data = res.data; 

  // 将字段数据存储到 dynamicFields
  dynamicFields.length = 0; // 清空之前的字段
  dynamicFields.push(...data); // 动态生成字段

  // 初始化 formState，动态添加字段
  data.forEach(item => {
    formState[item] = ''; // 每个字段初始化为空字符串
  });
};

// 提交处理
const handleSubmit = async () => {
  const formData = new FormData();
  formData.append('username', userStore.username);
  // 将 formState 中的每个字段添加到 FormData 中
  Object.keys(formState).forEach(key => {
    // 如果字段值为空，可以选择跳过或者设置默认值
    if (formState[key]) {
      formData.append(key, formState[key]);
    }
  });

  try {
    const res = await setInfoStore.setInfo(formData);
    // 处理后端响应
    if (res.status === 200) {
      message.success('Set Infomation successful!');
    } else {
      message.error('Set Infomation failed. Please check your infomation.');
    }
  } catch (error) {
    console.error('Error submitting form:', error);
  }
};


// 生命周期钩子
onMounted(() => {
  getInfo(); // 组件加载时获取字段信息
});
</script>

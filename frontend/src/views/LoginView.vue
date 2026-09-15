<template>
  <main class="page narrow">
    <el-card class="login-card">
      <h1>登录 RentFind</h1>
      <p class="hint">演示账号：tenant1 / tenant2（租客）、landlord1（房东），密码均为 123456</p>
      <el-form @submit.prevent="submit">
        <el-form-item>
          <el-input v-model="username" placeholder="用户名" autocomplete="username" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="password" type="password" placeholder="密码" show-password autocomplete="current-password" />
        </el-form-item>
        <el-button type="primary" class="full" :loading="loading" native-type="submit">登录</el-button>
      </el-form>
      <p v-if="error" class="error">{{ error }}</p>
    </el-card>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { login } from '../api/client';
import { setAuth } from '../stores/auth';

const route = useRoute();
const router = useRouter();
const username = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

async function submit() {
  if (!username.value || !password.value) {
    error.value = '请输入用户名和密码';
    return;
  }
  loading.value = true;
  error.value = '';
  try {
    const result = await login(username.value, password.value);
    setAuth(result.token, result.user);
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/';
    router.push(redirect);
  } catch (err) {
    error.value = err instanceof Error ? err.message : '登录失败';
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <el-header class="app-header">
    <router-link to="/" class="brand">RentFind</router-link>
    <nav class="nav">
      <router-link to="/">房源列表</router-link>
      <router-link to="/favorites">我的收藏</router-link>
    </nav>
    <div class="account">
      <template v-if="auth.user">
        <el-tag size="small">{{ auth.user.role }}</el-tag>
        <span>{{ auth.user.username }}</span>
        <el-button size="small" text @click="logout">退出</el-button>
      </template>
      <el-button v-else size="small" type="primary" @click="router.push('/login')">登录</el-button>
    </div>
  </el-header>
  <router-view />
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { auth, clearAuth } from './stores/auth';

const router = useRouter();

function logout() {
  clearAuth();
  router.push('/');
}
</script>

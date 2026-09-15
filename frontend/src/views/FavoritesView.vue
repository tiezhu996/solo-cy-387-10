<template>
  <main class="page">
    <section class="toolbar">
      <div>
        <h1>我的收藏夹</h1>
        <p>共 {{ favorites.length }} 套收藏房源，失效房源不可预约。</p>
      </div>
    </section>
    <p v-if="error" class="error">{{ error }}</p>
    <el-empty v-if="!error && favorites.length === 0" description="还没有收藏，去房源列表看看吧" />
    <section class="grid">
      <el-card v-for="item in favorites" :key="item.id" shadow="hover" class="property-card">
        <template #header>
          <div class="card-header">
            <strong>{{ item.property.community }}</strong>
            <el-tag v-if="!item.valid" type="danger">已失效</el-tag>
            <el-tag v-else type="success">{{ item.property.status }}</el-tag>
          </div>
        </template>
        <p>{{ item.property.region }} · {{ item.property.layout }} · {{ item.property.area }}㎡</p>
        <p class="rent">¥{{ item.property.rent }}/月</p>
        <p v-if="!item.valid" class="invalid-tip">房源已下架，无法预约看房</p>
        <div class="card-actions">
          <el-button size="small" @click="router.push(`/properties/${item.propertyId}`)">查看详情</el-button>
          <el-button size="small" type="primary" :disabled="!item.valid" @click="book(item)">预约看房</el-button>
          <el-button size="small" type="danger" plain :loading="pendingId === item.propertyId" @click="remove(item)">
            取消收藏
          </el-button>
        </div>
      </el-card>
    </section>
    <p v-if="notice" class="notice">{{ notice }}</p>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { createBooking, getFavorites, setFavorite } from '../api/client';
import type { FavoriteItem } from '../types/domain';

const router = useRouter();
const favorites = ref<FavoriteItem[]>([]);
const error = ref('');
const notice = ref('');
const pendingId = ref<number | null>(null);

onMounted(async () => {
  try {
    favorites.value = await getFavorites();
  } catch (err) {
    error.value = err instanceof Error ? err.message : '收藏夹加载失败';
  }
});

async function remove(item: FavoriteItem) {
  if (pendingId.value !== null) return;
  pendingId.value = item.propertyId;
  try {
    await setFavorite(item.propertyId, false);
    favorites.value = favorites.value.filter((entry) => entry.id !== item.id);
  } catch (err) {
    notice.value = err instanceof Error ? err.message : '操作失败';
  } finally {
    pendingId.value = null;
  }
}

async function book(item: FavoriteItem) {
  if (!item.valid) return;
  try {
    const booking = await createBooking(item.propertyId, '周六 10:00');
    notice.value = `预约成功：${item.property.community} ${booking.slot}，状态 ${booking.status}`;
  } catch (err) {
    notice.value = err instanceof Error ? err.message : '预约失败';
  }
}
</script>

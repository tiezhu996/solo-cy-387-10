<template>
  <el-card shadow="hover" class="property-card">
    <template #header>
      <div class="card-header">
        <strong>{{ item.community }}</strong>
        <el-tag>{{ item.status }}</el-tag>
      </div>
    </template>
    <p>{{ item.region }} · {{ item.layout }} · {{ item.area }}㎡</p>
    <p class="rent">¥{{ item.rent }}/月，押金 ¥{{ item.deposit }}</p>
    <div class="facility-list">
      <el-tag v-for="facility in item.facilities" :key="facility" size="small">{{ facility }}</el-tag>
    </div>
    <div class="card-actions">
      <el-button size="small" @click="emit('view', item.id)">查看详情</el-button>
      <el-button
        size="small"
        :type="item.favorited ? 'warning' : 'default'"
        :loading="favoritePending"
        @click="emit('toggle-favorite', item)"
      >
        {{ item.favorited ? `★ 已收藏 (${item.favoriteCount})` : `☆ 收藏 (${item.favoriteCount})` }}
      </el-button>
    </div>
    <el-button type="primary" class="full" :disabled="!item.bookable" @click="emit('book', item)">预约看房</el-button>
  </el-card>
</template>

<script setup lang="ts">
import type { PropertyItem } from '../types/domain';

defineProps<{ item: PropertyItem; favoritePending?: boolean }>();
const emit = defineEmits<{
  (e: 'view', id: number): void;
  (e: 'toggle-favorite', item: PropertyItem): void;
  (e: 'book', item: PropertyItem): void;
}>();
</script>

<template>
  <main class="page">
    <el-button text @click="router.back()">← 返回</el-button>
    <p v-if="error" class="error">{{ error }}</p>
    <template v-if="property">
      <section class="detail">
        <el-carousel class="photos" height="320px">
          <el-carousel-item v-for="(photo, index) in property.photos" :key="index">
            <img :src="photo" :alt="`${property.community} 照片 ${index + 1}`" class="photo" />
          </el-carousel-item>
        </el-carousel>
        <div class="detail-body">
          <div class="card-header">
            <h1>{{ property.community }}</h1>
            <el-tag :type="property.bookable ? 'success' : 'danger'">{{ property.status }}</el-tag>
          </div>
          <p>{{ property.region }} · {{ property.layout }} · {{ property.area }}㎡ · {{ property.payment }}</p>
          <p class="rent">¥{{ property.rent }}/月，押金 ¥{{ property.deposit }}</p>
          <h3>房源描述</h3>
          <p>{{ property.description }}</p>
          <h3>配套设施</h3>
          <div class="facility-list">
            <el-tag v-for="facility in property.facilities" :key="facility" size="small">{{ facility }}</el-tag>
          </div>
          <h3>房东联系方式</h3>
          <p>{{ property.landlordPhone }}</p>
          <el-alert v-if="!property.bookable" type="error" :closable="false" title="该房源已下架，无法预约看房" />
          <div class="actions">
            <el-button
              :type="property.favorited ? 'warning' : 'default'"
              :loading="favoritePending"
              @click="toggleFavorite"
            >
              {{ property.favorited ? `★ 已收藏 (${property.favoriteCount})` : `☆ 收藏 (${property.favoriteCount})` }}
            </el-button>
            <el-select v-model="slot" class="slot-select" :disabled="!property.bookable">
              <el-option v-for="option in slots" :key="option" :label="option" :value="option" />
            </el-select>
            <el-button type="primary" :disabled="!property.bookable" :loading="bookingPending" @click="book">
              预约看房
            </el-button>
            <el-button
              v-if="auth.user?.role === '房东' && property.bookable"
              type="danger"
              plain
              :loading="delistPending"
              @click="delist"
            >
              下架房源
            </el-button>
          </div>
          <p v-if="notice" class="notice">{{ notice }}</p>
        </div>
      </section>
    </template>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { createBooking, delistProperty, getProperty, setFavorite } from '../api/client';
import { auth } from '../stores/auth';
import type { PropertyItem } from '../types/domain';

const props = defineProps<{ id: string }>();
const router = useRouter();

const property = ref<PropertyItem | null>(null);
const error = ref('');
const notice = ref('');
const slots = ['周六 10:00', '周六 14:00', '周日 10:00', '周日 14:00'];
const slot = ref(slots[0]);
const favoritePending = ref(false);
const bookingPending = ref(false);
const delistPending = ref(false);

onMounted(async () => {
  try {
    property.value = await getProperty(Number(props.id));
  } catch (err) {
    error.value = err instanceof Error ? err.message : '房源加载失败';
  }
});

function requireLogin(): boolean {
  if (auth.token) return true;
  router.push({ name: 'login', query: { redirect: `/properties/${props.id}` } });
  return false;
}

async function toggleFavorite() {
  if (!property.value || favoritePending.value || !requireLogin()) return;
  favoritePending.value = true;
  try {
    const state = await setFavorite(property.value.id, !property.value.favorited);
    property.value.favorited = state.favorited;
    property.value.favoriteCount = state.favoriteCount;
  } catch (err) {
    notice.value = err instanceof Error ? err.message : '操作失败';
  } finally {
    favoritePending.value = false;
  }
}

async function book() {
  if (!property.value || !property.value.bookable) return;
  bookingPending.value = true;
  notice.value = '';
  try {
    const booking = await createBooking(property.value.id, slot.value);
    notice.value = `预约成功：${booking.slot}，状态 ${booking.status}`;
  } catch (err) {
    notice.value = err instanceof Error ? err.message : '预约失败';
  } finally {
    bookingPending.value = false;
  }
}

async function delist() {
  if (!property.value) return;
  delistPending.value = true;
  try {
    property.value = await delistProperty(property.value.id);
    notice.value = '房源已下架，收藏夹中该房源已标记失效';
  } catch (err) {
    notice.value = err instanceof Error ? err.message : '下架失败';
  } finally {
    delistPending.value = false;
  }
}
</script>

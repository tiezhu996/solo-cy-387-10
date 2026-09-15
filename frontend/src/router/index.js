import { createRouter, createWebHistory } from 'vue-router';
import { auth } from '../stores/auth';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import PropertyDetailView from '../views/PropertyDetailView.vue';
import FavoritesView from '../views/FavoritesView.vue';
export const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'home', component: HomeView },
        { path: '/login', name: 'login', component: LoginView },
        { path: '/properties/:id', name: 'property-detail', component: PropertyDetailView, props: true },
        { path: '/favorites', name: 'favorites', component: FavoritesView, meta: { requiresAuth: true } },
    ],
});
router.beforeEach((to) => {
    if (to.meta.requiresAuth && !auth.token) {
        return { name: 'login', query: { redirect: to.fullPath } };
    }
    return true;
});

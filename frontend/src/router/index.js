import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import MovieView from '@/views/MovieView.vue';
import SessionsView from '@/views/SessionsView.vue';
import BasketView from '@/views/BasketView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes : [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/movies/:id',
      name: 'movieDetails',
      component: MovieView, props: true
    },
    {
      path: '/sessions',
      name: 'sessions',
      component: SessionsView, props: true,
    },
    {
      path: '/basket',
      name: 'basket',
      component: BasketView, props: true,
    },
  ]
});

export default router;

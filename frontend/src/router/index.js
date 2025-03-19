import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import MovieView from '@/views/MovieView.vue';
import SessionsView from '@/views/SessionsView.vue';
import BasketView from '@/views/BasketView.vue';
import PaymentView from '@/views/PaymentView.vue';
import PaymentSuccessView from '@/views/PaymentSuccessView.vue';
import PaymentCancelView from '@/views/PaymentCancelView.vue';
import NotFoundView from '@/views/NotFoundView.vue';

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
    {
      path: '/payment/:user_id',
      name: 'payment',
      component: PaymentView,
      props: true
    },
    {
      path: '/payment/success',
      name: 'paymentSuccess',
      component: PaymentSuccessView,
      props: true
    },
    {
      path: '/payment/cancel',
      name: 'paymentCancel',
      component: PaymentCancelView,
      props: true
    },
    { path: '/:pathMatch(.*)*', 
      name: 'notFound', 
      component: NotFoundView
    }
  ]
});

export default router;

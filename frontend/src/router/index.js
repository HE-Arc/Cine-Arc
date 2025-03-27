import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import MovieView from '@/views/MovieView.vue';
import SessionsView from '@/views/SessionsView.vue';
import BasketView from '@/views/BasketView.vue';
import PaymentSuccessView from '@/views/PaymentSuccessView.vue';
import PaymentCancelView from '@/views/PaymentCancelView.vue';
import NotFoundView from '@/views/NotFoundView.vue';
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import AboutViewVue from '@/views/AboutView.vue';

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
      meta: { requiresAuth: true },
    },
    {
      path: '/basket',
      name: 'basket',
      component: BasketView, props: true,
      meta: { requiresAuth: true },
    },
    {
      path: "/login",
      name: "login",
      component: LoginView
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView
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
    },
    { path: '/about',
      name: 'About',
      component: AboutViewVue
    }
  ]
});

// Vérifier l'authentification avant chaque navigation
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("token");

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login"); // Redirige vers le login si non connecté
  } else {
    next();
  }
});

export default router;

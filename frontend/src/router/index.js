import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import MovieView from '@/views/MovieView.vue';
import LoginView from '@/views/LoginView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes : [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: '/movies/:id',
      name: 'movieDetails',
      component: MovieView, props: true
    },
    {
      path: '/sessions',
      name: 'sessions',
      component: () => import('../views/SessionsView.vue'),
      meta: { requiresAuth: true },
    },
  ]
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("accessToken");

  // Si l'utilisateur essaie d'accéder à /login alors qu'il est connecté, redirection vers la home
  if (to.path === "/login" && token) {
    next("/");
  }

  // Pour les routes protégées, on vérifie si l'utilisateur est connecté
  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else {
    next();
  }
});

export default router;

import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import MovieView from '@/views/MovieView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes : [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {

      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/sessions',
      name: 'sessions',
      component: () => import('../views/SessionsView.vue'), 
    },
  ],
})

      path: '/movies/:id',
      name: 'movieDetails',
      component: MovieView, props: true
    },
  ]
});


export default router;

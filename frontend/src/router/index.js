import { createRouter, createWebHistory } from 'vue-router';
// Importing all the views used in the application
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

// Creating the Vue Router instance
const router = createRouter({
  // Using HTML5 history mode for clean URLs
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/', // Root path for the home page
      name: 'home',
      component: HomeView
    },
    {
      path: '/movies/:id', // Dynamic route for movie details
      name: 'movieDetails',
      component: MovieView,
      props: true // Pass route params as props to the component
    },
    {
      path: '/sessions', // Path for sessions page
      name: 'sessions',
      component: SessionsView,
      props: true,
      meta: { requiresAuth: true }, // Requires authentication
    },
    {
      path: '/basket', // Path for the basket page
      name: 'basket',
      component: BasketView,
      props: true,
      meta: { requiresAuth: true }, // Requires authentication
    },
    {
      path: "/login", // Path for the login page
      name: "login",
      component: LoginView
    },
    {
      path: "/register", // Path for the registration page
      name: "register",
      component: RegisterView
    },
    {
      path: '/payment/success', // Path for payment success page
      name: 'paymentSuccess',
      component: PaymentSuccessView,
      props: true
    },
    {
      path: '/payment/cancel', // Path for payment cancellation page
      name: 'paymentCancel',
      component: PaymentCancelView,
      props: true
    },
    {
      path: '/:pathMatch(.*)*', // Catch-all route for 404 Not Found
      name: 'notFound',
      component: NotFoundView
    },
    {
      path: '/about', // Path for the About page
      name: 'About',
      component: AboutViewVue
    }
  ]
});

// Global navigation guard to check authentication before each route
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("token"); // Check if a token exists in localStorage

  if (to.meta.requiresAuth && !isAuthenticated) {
    next("/login"); // Redirect to login page if not authenticated
  } else {
    next(); // Proceed to the next route
  }
});

// Exporting the router instance to be used in the Vue app
export default router;

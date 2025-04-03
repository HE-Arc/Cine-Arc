<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
    <!-- Brand name -->
    <a class="navbar-brand" href="/">Ciné-Arc</a>

    <!-- Toggler button for mobile view -->
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <!-- Show "Add Sessions" only for administrators -->
        <li class="nav-item" v-if="isAdmin">
          <a class="nav-link" href="/sessions">Ajouter des séances</a>
        </li>
      </ul>

      <!-- Section to align Basket and Log In/Logout to the right -->
      <ul class="navbar-nav ms-auto">
        <!-- About link -->
        <li class="nav-item">
          <a class="nav-link" href="/about">A propos</a>
        </li>

        <!-- Basket link with an icon -->
        <li class="nav-item">
          <a class="nav-link" href="/basket">
            <i class="bi bi-cart"></i> Panier
          </a>
        </li>

        <!-- Logout button if the user is authenticated -->
        <li class="nav-item" v-if="isAuthenticated">
          <button class="nav-link" @click="logout">Se Déconnecter</button>
        </li>

        <!-- Login link if the user is not authenticated -->
        <li class="nav-item" v-else>
          <a class="nav-link" href="/login">Se connecter</a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import Swal from "sweetalert2";

const isLoggedIn = ref(!!localStorage.getItem("token")); // Reactive variable to check if the user is logged in
const router = useRouter(); // Vue Router instance

export default {
  data() {
    return {
      isAuthenticated: false, // Tracks if the user is authenticated
      isAdmin: false, // Tracks if the user is an administrator
    };
  },
  async mounted() {
    // Fetch user information when the component is mounted
    await this.fetchUser();
  },
  methods: {
    async fetchUser() {
      try {
        const API_URL = import.meta.env.VITE_API_URL; // API base URL from environment variables
        const token = localStorage.getItem("token"); // Retrieve the token from localStorage

        if (!token) {
          // If no token is found, set authentication and admin status to false
          this.isAuthenticated = false;
          return;
        }

        // Make an API call to fetch user information
        const response = await axios.get(`${API_URL}/auth/user/`, {
          headers: { Authorization: `Bearer ${token}` }, // Include the token in the request headers
        });

        // Update authentication and admin status based on the response
        this.isAuthenticated = true;
        this.isAdmin = response.data.is_superuser;

      } catch (error) {
        // Handle errors by resetting authentication and admin status
        this.isAuthenticated = false;
        this.isAdmin = false;
      }
    },
    logout() {
      // Remove the token from localStorage and reset authentication and admin status
      localStorage.removeItem("token");
      this.isLoggedIn = false;
      this.isAuthenticated = false;
      this.isAdmin = false;

      // Show a success message using SweetAlert2
      Swal.fire({
        title: "Déconnexion réussie",
        text: "Vous avez été déconnecté.",
        icon: "success",
        timer: 2000,
        showConfirmButton: false,
      });

      // Redirect to the login page after a short delay and reload the page
      setTimeout(() => {
        router.push("/login").then(() => {
          location.reload();
        });
      }, 2000);
    }
  }
};
</script>

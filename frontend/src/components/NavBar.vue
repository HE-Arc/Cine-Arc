<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="/">Ciné-Arc</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <!-- Afficher Add Sessions uniquement pour les administrateurs -->
        <li class="nav-item" v-if="isAdmin">
          <a class="nav-link" href="/sessions">Ajouter des séances</a>
        </li>
      </ul>

      <!-- Section pour aligner Basket et Log In/Logout à droite -->
      <ul class="navbar-nav ms-auto">

        <li class="nav-item">
          <a class="nav-link" href="/about">A propos</a>
        </li>

        <li class="nav-item">
          <a class="nav-link" href="/basket">
            <i class="bi bi-cart"></i> Panier
          </a>
        </li>

        <li class="nav-item" v-if="isAuthenticated">
          <button class="nav-link" @click="logout">Se Déconnecter</button>
        </li>

        <li class="nav-item" v-else>
          <a class="nav-link" href="/login">Se connecter</a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      isAuthenticated: false,
      isAdmin: false,
    };
  },
  async mounted() {
    await this.fetchUser();
  },
  methods: {
    async fetchUser() {
      try {
        const API_URL = import.meta.env.VITE_API_URL;
        const token = localStorage.getItem("token");

        if (!token) {
          this.isAuthenticated = false;
          return;
        }

        const response = await axios.get(`${API_URL}/auth/user/`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        this.isAuthenticated = true;
        this.isAdmin = response.data.is_superuser;

      } catch (error) {
        console.error("Erreur lors de la récupération des infos utilisateur:", error);
        this.isAuthenticated = false;
        this.isAdmin = false;
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.isAuthenticated = false;
      this.isAdmin = false;
      window.location.href = "/";
    }
  }
};
</script>

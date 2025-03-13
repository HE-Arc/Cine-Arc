<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="/">Ciné-Arc</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="/sessions">Add Sessions</a>
        </li>

        <li class="nav-item">
          <a class="nav-link" href="/basket">
            <i class="bi bi-cart"></i> Basket
          </a>
        </li>

        <!-- Afficher le bouton Login si l'utilisateur n'est pas connecté -->
        <li class="nav-item" v-if="!isAuthenticated">
          <a class="nav-link" href="/login">Log In</a>
        </li>

        <!-- Afficher le bouton Logout si l'utilisateur est connecté -->
        <li class="nav-item" v-if="isAuthenticated">
          <button class="nav-link btn btn-danger text-white" @click="logout">Log Out</button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem("accessToken"); // Vérifie si un token est présent
    },
  },
  methods: {
    logout() {
      // Supprime le token et redirige vers la page de connexion
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
/* Ajout d'un style pour le bouton Logout */
.btn-danger {
  border: none;
  cursor: pointer;
}
</style>

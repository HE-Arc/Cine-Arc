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

        <!-- Afficher Log In si l'utilisateur n'est pas connecté -->
        <li class="nav-item" v-if="!isAuthenticated">
          <a class="nav-link" href="/login">Log In</a>
        </li>

        <!-- Afficher Log Out si l'utilisateur est connecté -->
        <li class="nav-item" v-if="isAuthenticated">
          <button class="nav-link btn btn-danger text-white" @click="logout">Log Out</button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import { ref, watchEffect } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "NavBar",
  setup() {
    const router = useRouter();
    const isAuthenticated = ref(!!localStorage.getItem("accessToken")); // État réactif

    // Surveiller le localStorage pour détecter les changements
    watchEffect(() => {
      isAuthenticated.value = !!localStorage.getItem("accessToken");
    });

    const logout = () => {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      isAuthenticated.value = false; // Mettre à jour immédiatement
      router.push("/login");
    };

    return { isAuthenticated, logout };
  },
};
</script>

<style scoped>
.btn-danger {
  border: none;
  cursor: pointer;
}
</style>

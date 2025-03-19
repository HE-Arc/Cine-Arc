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

        <li class="nav-item" v-if="isAuthenticated">
          <button class="nav-link btn btn-danger" @click="logout">Se Déconnecter</button>
        </li>

        <li class="nav-item" v-else>
          <a class="nav-link" href="/login">Log In</a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
export default {
  name: "NavBar",
  setup() {
    const store = useStore();
    const router = useRouter();

    const isAuthenticated = computed(() => !!store.state.token);

    const logout = () => {
      store.dispatch("logout");
      router.push("/login"); // Rediriger vers la page de connexion après déconnexion
    };

    return { isAuthenticated, logout };
  },
};
</script>

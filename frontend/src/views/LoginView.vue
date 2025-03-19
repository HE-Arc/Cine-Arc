<template>
  <div class="login-page">
    <div class="login-container">
      <div class="card p-4 shadow-sm">
        <h2 class="text-center mb-3">Connexion</h2>

        <form @submit.prevent="login">
          <!-- Champ Email -->
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input v-model="email" type="email" class="form-control" required placeholder="Entrez votre email" />
          </div>

          <!-- Champ Mot de passe -->
          <div class="mb-3">
            <label for="password" class="form-label">Mot de passe</label>
            <input v-model="password" type="password" class="form-control" required placeholder="••••••••" />
          </div>

          <!-- Checkbox "Se souvenir de moi" -->
          <div class="mb-3 form-check">
            <input type="checkbox" class="form-check-input" v-model="rememberMe" id="rememberMe" />
            <label class="form-check-label" for="rememberMe">Se souvenir de moi</label>
          </div>

          <!-- Bouton Se connecter -->
          <button type="submit" class="btn btn-primary w-100" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm"></span>
            Se connecter
          </button>

          <!-- Message d'erreur -->
          <p v-if="errorMessage" class="text-danger mt-2 text-center">{{ errorMessage }}</p>

          <!-- Lien pour s'inscrire -->
          <p class="mt-3 text-center">
            Pas de compte ? <router-link to="/register">Créez-en un ici</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";

export default {
  data() {
    return {
      email: localStorage.getItem("savedEmail") || "", // Récupération de l'email si "Se souvenir de moi" est coché
      password: "",
      rememberMe: !!localStorage.getItem("savedEmail"), // Si un email est enregistré, cocher la case
      errorMessage: "",
      loading: false,
    };
  },
  methods: {
    async login() {
  this.loading = true;
  this.errorMessage = "";

  try {
    console.log("Tentative de connexion avec :", {
      email: this.email.trim(),
      password: this.password.trim(), // Supprimer espaces invisibles
    });

    const response = await axios.post("http://127.0.0.1:8000/api/login/", {
      email: this.email.trim(),
      password: this.password.trim(),
    }, {
      headers: { "Content-Type": "application/json" },
    });

    console.log("Réponse de l'API :", response.data);

    localStorage.setItem("accessToken", response.data.access);
    localStorage.setItem("refreshToken", response.data.refresh);
    this.$router.push("/");
  } catch (error) {
    console.error("Erreur lors de la connexion :", error.response);
    this.errorMessage = error.response?.data?.error || "Identifiants incorrects";
  } finally {
    this.loading = false;
  }
},
  }
};
</script>

<style scoped>
/* Empêcher le scrolling vertical et mettre un fond blanc */
.login-page {
  height: 80vh; /* Prend toute la hauteur de l'écran */
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white; /* Fond blanc */
  overflow: hidden; /* Empêche le scroll vertical */
}

/* Conteneur du formulaire */
.login-container {
  width: 80%;
  max-width: 400px; /* Largeur du formulaire */
  padding: 20px;
}

/* Style de la carte (formulaire) */
.card {
  border-radius: 10px;
  width: 100%;
}

/* Style du bouton */
.btn-primary {
  font-weight: bold;
}

/* Animation de chargement */
.spinner-border {
  margin-right: 5px;
}
</style>

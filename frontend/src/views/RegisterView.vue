
<template>
  <div class="register-page">
    <div class="register-container">
      <div class="card p-4 shadow-sm">
        <h2 class="text-center mb-3">Inscription</h2>

        <form @submit.prevent="register">
          <!-- Champ Email -->
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input v-model="email" type="email" class="form-control" required placeholder="Entrez votre email" />
          </div>

          <!-- Champ Prénom -->
          <div class="mb-3">
            <label for="first_name" class="form-label">Prénom</label>
            <input v-model="first_name" type="text" class="form-control" required placeholder="Votre prénom" />
          </div>

          <!-- Champ Nom -->
          <div class="mb-3">
            <label for="last_name" class="form-label">Nom</label>
            <input v-model="last_name" type="text" class="form-control" required placeholder="Votre nom" />
          </div>

          <!-- Champ Mot de passe -->
          <div class="mb-3">
            <label for="password" class="form-label">Mot de passe</label>
            <input v-model="password" type="password" class="form-control" required placeholder="••••••••" />
          </div>

          <!-- Bouton S'inscrire -->
          <button type="submit" class="btn btn-success w-100" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm"></span>
            S'inscrire
          </button>

          <!-- Message d'erreur -->
          <p v-if="errorMessage" class="text-danger mt-2 text-center">{{ errorMessage }}</p>

          <!-- Lien pour retourner à la connexion -->
          <p class="mt-3 text-center">
            Déjà un compte ? <router-link to="/login">Connectez-vous ici</router-link>
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
      email: "",
      first_name: "",
      last_name: "",
      password: "",
      errorMessage: "",
      loading: false,
    };
  },
  methods: {
    async register() {
      this.loading = true;
      this.errorMessage = "";

      try {
        console.log("Tentative d'inscription avec :", {
          email: this.email,
          first_name: this.first_name,
          last_name: this.last_name,
          password: this.password,
        });

        await axios.post("http://127.0.0.1:8000/api/users/", {
          email: this.email,
          first_name: this.first_name,
          last_name: this.last_name,
          password: this.password,
        }, {
          headers: { "Content-Type": "application/json" },
        });

        console.log("Utilisateur créé avec succès");

        // Rediriger vers la page de connexion après l'inscription
        this.$router.push("/login");
      } catch (error) {
        console.error("Erreur lors de l'inscription :", error.response);
        this.errorMessage = error.response?.data?.error || "Erreur lors de l'inscription.";
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Empêcher le scrolling vertical et mettre un fond blanc */
.register-page {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: white;
  overflow: hidden;
}

/* Conteneur du formulaire */
.register-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
}

/* Style de la carte (formulaire) */
.card {
  border-radius: 10px;
  width: 100%;
}

/* Style du bouton */
.btn-success {
  font-weight: bold;
}
</style>

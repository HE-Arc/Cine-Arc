<template>
  <div class="login-container">
    <h2>Connexion</h2>
    <form @submit.prevent="login">
      <div>
        <label for="email">Email</label>
        <input v-model="email" type="email" required />
      </div>
      <div>
        <label for="password">Mot de passe</label>
        <input v-model="password" type="password" required />
      </div>
      <button type="submit">Se connecter</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        console.log("Tentative de connexion avec :", {
          email: this.email,
          password: this.password,
        }); // 🔍 Vérifier les données envoyées

        const response = await axios.post("http://127.0.0.1:8000/api/login/", {
          email: this.email,
          password: this.password,
        }, {
          headers: {
            "Content-Type": "application/json",
          },
        });

        console.log("Réponse de l'API :", response.data); // 🔍 Voir la réponse

        localStorage.setItem("accessToken", response.data.access);
        localStorage.setItem("refreshToken", response.data.refresh);

        this.$router.push("/");
      } catch (error) {
        console.error("Erreur lors de la connexion :", error.response);
        this.errorMessage = error.response?.data?.error || "Identifiants incorrects";
      }
    }
    ,
  },
};
</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.error {
  color: red;
}
</style>

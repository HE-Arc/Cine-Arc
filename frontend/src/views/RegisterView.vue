<template>
  <div class="container">
    <h2>Créer un compte</h2>

    <form @submit.prevent="register">
    <div class="form-group">
      <label>Nom d'utilisateur</label>
      <input v-model="username" type="text" class="form-control" required />
    </div>

    <div class="form-group">
      <label>Email</label>
      <input v-model="email" type="email" class="form-control" required />
    </div>

    <div class="form-group">
      <label>Mot de passe</label>
      <input v-model="password" type="password" class="form-control" required />
      <small class="text-muted">
      Doit contenir au moins 8 caractères et un caractère spécial (!@#$%^&*).
      </small>
    </div>

    <div class="form-group">
      <label>Confirmer le mot de passe</label>
      <input v-model="confirmPassword" type="password" class="form-control" required />
    </div>

    <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>

    <button type="submit" class="btn btn-primary">S'inscrire</button>
    </form>

    <p class="mt-3">
    Déjà un compte ? <router-link to="/login">Se connecter</router-link>
    </p>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter } from "vue-router";
import { ref } from "vue";
import Swal from "sweetalert2";

export default {
  setup() {
    const router = useRouter(); // Vue Router instance for navigation
    const username = ref(""); // Username input field
    const email = ref(""); // Email input field
    const password = ref(""); // Password input field
    const confirmPassword = ref(""); // Confirm password input field
    const errorMessage = ref(""); // Error message to display in the UI

    // Function to validate if the password meets the required criteria
    const isValidPassword = (pwd) => {
      return pwd.length >= 8 && /[!@#$%^&*]/.test(pwd);
    };

    // Function to handle user registration
    const register = async () => {
      errorMessage.value = ""; // Reset error message

      // Check if passwords match
      if (password.value !== confirmPassword.value) {
        errorMessage.value = "Les mots de passe ne correspondent pas.";
        return;
      }

      // Validate password strength
      if (!isValidPassword(password.value)) {
        Swal.fire({
        title: "Mot de passe invalide",
        text: "Le mot de passe doit contenir au moins 8 caractères et un caractère spécial (!@#$%^&*).",
        icon: "error",
        });
        return;
      }

      try {
        // API URL from environment variables
        const API_URL = import.meta.env.VITE_API_URL;

        // Send registration data to the backend
        const response = await axios.post(`${API_URL}/auth/register/`, {
        username: username.value,
        email: email.value,
        password: password.value,
        });

        // Show success message using SweetAlert2
        Swal.fire({
          title: "Inscription réussie !",
          text: response.data.message,
          icon: "success",
          timer: 2000,
          showConfirmButton: false,
          });

          // Redirect to login page after success
          setTimeout(() => {
          router.push("/login");
          }, 2000);
      } catch (error) {
        // Handle errors from the backend or server
        if (error.response && error.response.data && error.response.data.error) {
          Swal.fire({
            title: "Erreur",
            text: error.response.data.error,
            icon: "error",
          });
        } else {
          Swal.fire({
            title: "Erreur serveur",
            text: "Une erreur est survenue. Veuillez réessayer.",
            icon: "error",
          });
        }
      }
    };

    // Return variables and functions to the template
    return { username, email, password, confirmPassword, register, errorMessage };
  },
};
</script>

<style scoped>
.container {
  max-width: 400px; /* Limit the container width */
  margin: auto; /* Center the container */
  padding: 20px; /* Add padding inside the container */
}
</style>

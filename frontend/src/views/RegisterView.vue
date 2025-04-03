<template>
  <div class="register-wrapper d-flex justify-content-center pt-5 pb-5">
    <div class="card shadow p-4" style="width: 100%; max-width: 460px; height: 100%; max-height: 580px;">
      <h2 class="text-center mb-4">Créer un compte</h2>

      <form @submit.prevent="register">
        <!-- Nom d'utilisateur -->
        <div class="form-group mb-3">
          <label>Nom d'utilisateur</label>
          <input v-model="username" type="text" class="form-control" placeholder="ex: JeanDupont" required />
        </div>

        <!-- Email -->
        <div class="form-group mb-3">
          <label>Email</label>
          <input v-model="email" type="email" class="form-control" placeholder="ex: utilisateur@mail.com" required />
        </div>

        <!-- Mot de passe -->
        <div class="form-group mb-2">
          <label>Mot de passe</label>
          <input v-model="password" type="password" class="form-control" placeholder="••••••" required />
          <small class="text-muted">
            Doit contenir au moins 8 caractères et un caractère spécial (!@#$%^&*).
          </small>
        </div>

        <!-- Confirmation -->
        <div class="form-group mb-3">
          <label>Confirmer le mot de passe</label>
          <input v-model="confirmPassword" type="password" class="form-control" placeholder="••••••" required />
        </div>

        <!-- Message d'erreur global -->
        <p v-if="errorMessage" class="text-danger mb-2">{{ errorMessage }}</p>

        <!-- Bouton -->
        <button type="submit" class="btn btn-primary w-100">S'inscrire</button>

        <!-- Redirection login -->
        <p class="mt-4 text-center">
          Déjà un compte ? <router-link to="/login">Se connecter</router-link>
        </p>
      </form>
    </div>
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
.register-wrapper {
  background-color: #f4f6f9;
  min-height: 80vh;
}

.card {
  border-radius: 10px;
}

.form-control {
  border-radius: 6px;
  height: 45px;
  font-size: 15px;
}
</style>


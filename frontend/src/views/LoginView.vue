<template>
  <div class="container">
    <h2>Connexion</h2>
    <form @submit.prevent="validateForm">
      <!-- Email input field -->
      <div class="form-group mb-3">
        <label>Email</label>
        <input v-model="email" type="email" class="form-control" />
        <!-- Display email-specific error message -->
        <small v-if="emailError" class="text-danger">{{ emailError }}</small>
      </div>

      <!-- Password input field -->
      <div class="form-group mb-3">
        <label>Mot de passe</label>
        <input v-model="password" type="password" class="form-control" />
        <!-- Display password-specific error message -->
        <small v-if="passwordError" class="text-danger">{{ passwordError }}</small>
      </div>

      <!-- Submit button -->
      <button type="submit" class="btn btn-success">Se connecter</button>
      <!-- Display general error message -->
      <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>

      <!-- Link to the registration page -->
      <p class="mt-3">
        Pas encore de compte ? <router-link to="/register">Créer un compte</router-link>
      </p>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter } from "vue-router";
import { ref } from "vue";
import Swal from "sweetalert2";

export default {
  setup() {
    const router = useRouter();
    const email = ref(""); // Holds the email input value
    const password = ref(""); // Holds the password input value
    const errorMessage = ref(""); // Holds the general error message
    const emailError = ref(""); // Holds the email-specific error message
    const passwordError = ref(""); // Holds the password-specific error message

    // Function to validate the form inputs
    const validateForm = () => {
      // Reset error messages
      emailError.value = "";
      passwordError.value = "";
      errorMessage.value = "";

      let valid = true;

      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Regex for email format
      if (!email.value) {
        emailError.value = "L'email est requis."; // Email is required
        valid = false;
      } else if (!emailRegex.test(email.value)) {
        emailError.value = "Format de l'email invalide."; // Invalid email format
        valid = false;
      }

      // Password validation
      if (!password.value) {
        passwordError.value = "Le mot de passe est requis."; // Password is required
        valid = false;
      } else if (password.value.length < 4) {
        passwordError.value = "Le mot de passe doit faire au moins 6 caractères."; // Password must be at least 6 characters
        valid = false;
      }

      // If the form is valid, proceed to login
      if (valid) {
        login();
      }
    };

    // Function to handle the login process
    const login = async () => {
      try {
        const API_URL = import.meta.env.VITE_API_URL; // Get the API URL from environment variables
        const response = await axios.post(`${API_URL}/auth/login/`, {
          email: email.value,
          password: password.value,
        });

        // Store the token in localStorage
        localStorage.setItem("token", response.data.access);
        // Set the default Authorization header for axios
        axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.access}`;

        // Show a success message using SweetAlert2
        Swal.fire({
          title: "Connexion réussie !",
          text: "Bienvenue, vous allez être redirigé.",
          icon: "success",
          timer: 2000,
          showConfirmButton: false,
        });

        // Redirect to the home page after a short delay
        setTimeout(() => {
          router.push("/").then(() => {
            location.reload(); // Reload the page to refresh the state
          });
        }, 2000);
      } catch (error) {
        // Display an error message if login fails
        errorMessage.value = "Email ou mot de passe incorrect.";
        Swal.fire({
          title: "Erreur",
          text: "Email ou mot de passe incorrect.",
          icon: "error",
        });
      }
    };

    return {
      email,
      password,
      login,
      validateForm,
      errorMessage,
      emailError,
      passwordError,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
}
</style>

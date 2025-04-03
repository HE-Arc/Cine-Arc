<template>
  <div class="container mt-5 text-center">
    <!-- Display a success message for the payment -->
    <h2>✅ Paiement Réussi !</h2>
    <p>Votre paiement a été confirmé et vos billets sont maintenant réservés.</p>
    <!-- Link to navigate back to the homepage -->
    <router-link to="/" class="btn btn-primary">Retour à l'accueil</router-link>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import axios from "axios";

onMounted(async () => {
  try {
    const API_URL = import.meta.env.VITE_API_URL; // Retrieve the API base URL from environment variables

    // Fetch the currently logged-in user
    const userResponse = await axios.get(`${API_URL}/auth/user/`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }, // Include the authorization token
    });

    // Update the cart after the payment is successful
    await axios.post(
      `${API_URL}/payment/success/`,
      {}, // Send an empty object in the POST request body
      {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }, // Include the authorization token
      }
    );
  } catch (error) {
    // Handle errors during the API calls
  }
});
</script>

<style scoped>
.container {
  max-width: 600px; /* Set a maximum width for the container */
  margin: auto; /* Center the container horizontally */
  padding: 20px; /* Add padding inside the container */
}
</style>

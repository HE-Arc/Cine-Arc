<template>
  <!-- Container for the payment cancellation message -->
  <div class="cancel-container">
    <!-- Display a cancellation message with an icon -->
    <h2>❌ Paiement annulé</h2>
    <!-- Inform the user about retrying or modifying their cart -->
    <p>Vous pouvez réessayer ou modifier votre panier.</p>
    <!-- Link to navigate back to the basket page -->
    <router-link to="/basket">Retour au panier</router-link>
  </div>
</template>

<style scoped>
/* Styling for the cancellation message container */
.cancel-container {
  text-align: center; /* Center align the text */
  padding: 20px; /* Add padding around the container */
}
</style>

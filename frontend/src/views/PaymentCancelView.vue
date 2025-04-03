<template>
  <!-- Container for the payment cancellation message -->
  <div class="cancel-container">
    <h2>❌ Paiement annulé</h2>
    <p>Vous pouvez réessayer ou modifier votre panier.</p>
    <router-link to="/basket">Retour au panier</router-link>
  </div>
</template>

<style scoped>
.cancel-container {
  text-align: center; /* Center align the text */
  padding: 20px; /* Add padding around the container */
}
</style>

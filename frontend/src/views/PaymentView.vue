<template>
  <div class="payment-container">
    <h2>Paiement</h2>
    <p>Montant total : <strong>{{ totalAmount }} CHF</strong></p>
    <button @click="processPayment" :disabled="loading">
      {{ loading ? "Redirection vers Stripe..." : "Payer avec Stripe" }}
    </button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";
import { useRoute } from "vue-router";
import { ref, onMounted } from "vue";

export default {
  setup() {
    const route = useRoute();
    const userId = route.params.user_id;
    const totalAmount = ref(0);
    const loading = ref(false);
    const errorMessage = ref("");

    // Récupérer le montant total
    const fetchTotalAmount = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/payment/${userId}/`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        totalAmount.value = response.data.total;
      } catch (error) {
        console.error("Erreur lors de la récupération du montant :", error);
      }
    };

    // Rediriger vers Stripe
    const processPayment = async () => {
      loading.value = true;
      try {
        const response = await axios.get(`http://localhost:8000/api/payment/checkout/${userId}/`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        window.location.href = response.data.checkout_url;
      } catch (error) {
        errorMessage.value = "Erreur lors du paiement.";
        console.error(error);
      } finally {
        loading.value = false;
      }
    };

    onMounted(fetchTotalAmount);

    return { totalAmount, processPayment, loading, errorMessage };
  },
};
</script>


<style scoped>
.payment-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  text-align: center;
  background: #222;
  color: white;
  border-radius: 10px;
}

button {
  background-color: #ffcc00;
  border: none;
  padding: 10px 20px;
  font-size: 18px;
  cursor: pointer;
  border-radius: 5px;
}

button:disabled {
  background-color: grey;
  cursor: not-allowed;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>

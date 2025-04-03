<template>
  <div class="container mt-5">
    <h2>Mon Panier</h2>
    <div v-if="baskets.length > 0">
      <div class="list-group">
        <div v-for="basket in baskets" :key="basket.id" class="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <strong>{{ basket.session.movie.title }}</strong>
            <br> Séance : {{ formatDate(basket.session.date_hour) }} à {{ formatTime(basket.session.date_hour) }} - Salle {{ basket.session.room.name }}
          </div>
          <div class="d-flex align-items-center">
            <input
              type="number"
              class="form-control form-control-sm mx-2 text-center"
              style="width: 60px;"
              v-model="basket.quantity"
              :min="1"
              :max="basket.session.room.capacity"
              @blur="updateQuantity(basket)"
              @keydown.enter="updateQuantity(basket)"
            />
            <button class="btn btn-danger btn-sm ml-2" @click="removeBasketItem(basket)">Supprimer</button>
          </div>
        </div>
      </div>

      <!-- Total amount of the basket -->
      <div class="mt-3 d-flex justify-content-between align-items-center">
        <button class="btn btn-success" @click="processPayment" :disabled="loading">
          {{ loading ? "Redirection vers Stripe..." : "Payer avec Stripe" }}
        </button>
        <h4 class="mb-0">Total : {{ totalAmount }}.- CHF</h4>
      </div>
    </div>
    <div v-else>
      <p>Votre panier est vide.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      baskets: [],
      loading: false,
    };
  },
  computed: {
    // Calculate the total amount of the basket
    totalAmount() {
      return this.baskets.reduce((total, basket) => total + basket.quantity * 16, 0);
    }
  },
  async mounted() {
    // Fetch the basket data when the component is mounted
    await this.fetchBasket();
  },
  methods: {
    async fetchBasket() {
      try {
        const API_URL = import.meta.env.VITE_API_URL;
        const token = localStorage.getItem("token"); // Retrieve the token

        const response = await axios.get(`${API_URL}/basket/`, {
          headers: {
            'Authorization': `Bearer ${token}` // Add the token
          }
        });

        this.baskets = response.data;
      } catch (error) {
        Swal.fire("Erreur", "Impossible de charger votre panier.", "error");
      }
    },
    async processPayment() {
      this.loading = true; // Display "Redirecting to Stripe..."

      try {
        const API_URL = import.meta.env.VITE_API_URL;
        const token = localStorage.getItem("token");

        // API call to get the Stripe payment URL
        const response = await axios.get(`${API_URL}/payment/checkout/`, {
          headers: { Authorization: `Bearer ${token}` }
        });

        // Redirect to Stripe
        window.location.href = response.data.checkout_url;
      } catch (error) {
        Swal.fire("Erreur", "Une erreur est survenue. Veuillez réessayer.", "error");
      } finally {
        this.loading = false;
      }
    },
    // Format the date in "fr-FR" locale
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString("fr-FR");
    },
    // Format the time in "fr-FR" locale
    formatTime(dateString) {
      const date = new Date(dateString);
      return date.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
    },
    async updateQuantity(basket) {
      const newQuantity = parseInt(basket.quantity, 10);

      // Validate the quantity
      if (isNaN(newQuantity) || newQuantity < 1 || newQuantity > basket.session.room.capacity) {
        basket.quantity = Math.max(1, Math.min(basket.quantity, basket.session.room.capacity));
        Swal.fire("Attention", `La quantité doit être entre 1 et ${basket.session.room.capacity}.`, "warning");
        return;
      }

      try {
        const API_URL = import.meta.env.VITE_API_URL;
        const token = localStorage.getItem("token");
        await axios.patch(`${API_URL}/basket/${basket.id}/`, {
          quantity: newQuantity
        }, {
          headers: {
            Authorization: `Bearer ${token}` // Add the token here
          }
        });

        basket.quantity = newQuantity;
        Swal.fire("Succès", "Quantité mise à jour.", "success");
      } catch (error) {
        Swal.fire("Erreur", "Impossible de mettre à jour la quantité.", "error");
      }
    },
    async removeBasketItem(basket) {
      Swal.fire({
        title: "Êtes-vous sûr ?",
        text: "Cette action supprimera cet article du panier.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Oui, supprimer !",
        cancelButtonText: "Annuler",
      }).then(async (result) => {
        if (result.isConfirmed) {
          try {
            const API_URL = import.meta.env.VITE_API_URL;
            const token = localStorage.getItem("token"); // Retrieve the token

            if (!token) {
              Swal.fire("Erreur", "Vous devez être connecté pour supprimer un article du panier.", "error");
              return;
            }

            await axios.delete(`${API_URL}/basket/${basket.id}/`, {
              headers: { Authorization: `Bearer ${token}` }, // Add the token here
            });

            // Remove the item from the basket list
            this.baskets = this.baskets.filter((item) => item.id !== basket.id);
            Swal.fire("Supprimé !", "L'article a été retiré du panier.", "success");
          } catch (error) {
            Swal.fire("Erreur", "Impossible de supprimer l'article.", "error");
          }
        }
      });
    },
    async submitBasket() {
      if (this.baskets.length === 0) {
        alert('Votre panier est vide.');
        return;
      }

      try {
        const API_URL = import.meta.env.VITE_API_URL;

        // Update each basket item
        for (const basket of this.baskets) {
          const basketData = {
            session: basket.session.id,
            user: basket.user.id,
            quantity: basket.quantity,
          };

          await axios.patch(`${API_URL}/basket/${basket.id}/`, basketData, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
              'Content-Type': 'application/json'
            }
          });
        }

        alert('Panier mis à jour avec succès');
      } catch (error) {
        alert('Une erreur est survenue lors de la mise à jour du panier.');
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 0 auto;
}
</style>

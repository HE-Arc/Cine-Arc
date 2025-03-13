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

      <!-- Montant total du panier -->
      <div class="mt-3 d-flex justify-content-between align-items-center">
        <button class="btn btn-success" @click="submitBasket">Valider le panier</button>
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

export default {
  data() {
    return {
      baskets: [],
    };
  },
  computed: {
    totalAmount() {
      return this.baskets.reduce((total, basket) => total + basket.quantity * 16, 0);
    }
  },
  async mounted() {
    await this.fetchBasket();
  },
  methods: {
    async fetchBasket() {
      try {
        const API_URL = import.meta.env.VITE_API_URL;
        const response = await axios.get(`${API_URL}/basket/`);
        this.baskets = response.data;
      } catch (error) {
        console.error('Erreur lors de la récupération du panier:', error);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString("fr-FR");
    },
    formatTime(dateString) {
      const date = new Date(dateString);
      return date.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
    },
    async updateQuantity(basket) {
      console.log('Basket ID:', basket.id);
      console.log('New Quantity:', basket.quantity);

      const newQuantity = parseInt(basket.quantity, 10);

      if (isNaN(newQuantity) || newQuantity < 1 || newQuantity > basket.session.room.capacity) {
        basket.quantity = Math.max(1, Math.min(basket.quantity, basket.session.room.capacity));
        alert(`La quantité doit être entre 1 et ${basket.session.room.capacity}.`);
        return;
      }

      try {
        const API_URL = import.meta.env.VITE_API_URL;
        await axios.patch(`${API_URL}/basket/${basket.id}/`, {
          quantity: newQuantity
        });

        basket.quantity = newQuantity;
      } catch (error) {
        console.error('Erreur lors de la mise à jour du panier:', error);
      }
    },
    async removeBasketItem(basket) {
      try {
        const API_URL = import.meta.env.VITE_API_URL;
        await axios.delete(`${API_URL}/basket/${basket.id}/`);
        this.baskets = this.baskets.filter(item => item.id !== basket.id);
      } catch (error) {
        console.error('Erreur lors de la suppression du panier:', error);
      }
    },
    async submitBasket() {
      if (this.baskets.length === 0) {
        alert('Votre panier est vide.');
        return;
      }

      try {
        const API_URL = import.meta.env.VITE_API_URL;

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
        console.error('Erreur lors de la soumission du panier:', error.response ? error.response.data : error.message);
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

<template>
  <div class="container mt-5">
    <div class="row">
      <!-- Encadré gauche pour les informations du film -->
      <div class="col-md-4">
        <div v-if="movie" class="card movie-card">
          <div class="card-body">
            <div class="card mb-3">
              <img :src="movie.picture_url" :alt="movie.title" class="card-img-top movie-img" />
            </div>
            <h5 class="card-title">{{ movie.title }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ movie.release_date }}</h6>
            <p><strong>Durée :</strong> {{ movie.duration }} min</p>
            <p><strong>Genre :</strong> {{ movie.type }}</p>
            <p><strong>Note :</strong>  {{ movie.rating }} / 10 ⭐</p>
          </div>
        </div>
      </div>

      <!-- Conteneur central pour le synopsis et les séances -->
      <div class="col-md-8">
        <div v-if="movie" class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">Synopsis</h5>
            <p>{{ movie.synopsis }}</p>
          </div>
        </div>

        <!-- Séances disponibles -->
        <div class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">Séances disponibles</h5>
            <div v-if="filteredSessions.length > 0">
              <ul class="list-group">
                <li v-for="session in filteredSessions" :key="session.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <strong>{{ session.formattedDate }}</strong> - {{ session.room.name }}
                  </div>
                  <div class="d-flex align-items-center">
                    <!-- Champ de saisie pour modifier le nombre de billets -->
                    <input
                      type="number"
                      :value="getTicketsCount(session)"
                      :max="session.room.capacity"
                      min="0"
                      class="form-control form-control-sm"
                      @input="updateTicketCount(session, $event.target.value)"
                    />
                    <button @click="addToBasket(session)" class="btn btn-sm btn-primary ml-2">Ajouter</button>
                  </div>
                </li>
              </ul>
            </div>
            <div v-else>
              <p>Aucune séance n'est disponible pour ce film</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      movie: null,
      sessions: [],
      userId: null,
    };
  },
  async mounted() {
    try {
      const API_URL = import.meta.env.VITE_API_URL;

      // Récupérer les détails du film
      const movieResponse = await axios.get(`${API_URL}/movies/${this.$route.params.id}`);
      this.movie = movieResponse.data;

      // Récupérer toutes les séances
      const sessionsResponse = await axios.get(`${API_URL}/sessions`);
      this.sessions = sessionsResponse.data;
    } catch (error) {
      console.error("Error fetching movie or session details:", error);
    }
  },
  computed: {
    // Filtrer les séances pour n'afficher que celles correspondant au film actuel
    filteredSessions() {
      if (!this.movie || !this.sessions) return [];

      return this.sessions
        .filter(session => session.movie && session.movie.id === this.movie.id)
        .map(session => {
          return {
            ...session,
            formattedDate: this.formatDate(session.date_hour)
          };
        });
    }
  },
  methods: {
    formatDate(isoString) {
      const date = new Date(isoString);
      const formattedDate = date.toLocaleDateString("fr-FR", {
        day: "2-digit",
        month: "long",
        year: "numeric"
      });
      const formattedTime = date.toLocaleTimeString("fr-FR", {
        hour: "2-digit",
        minute: "2-digit"
      });
      return `Le ${formattedDate} à ${formattedTime}`;
    },

    // Retourne le nombre de billets actuel pour une séance
    getTicketsCount(session) {
      return session.quantity || 0;
    },

    // Mettre à jour le nombre de billets pour une séance
    updateTicketCount(session, newCount) {
      newCount = parseInt(newCount, 10);
      if (isNaN(newCount) || newCount < 0) {
        newCount = 0;
      }
      if (newCount > session.room.capacity) {
        newCount = session.room.capacity; // Ne pas dépasser la capacité de la salle
      }

      session.quantity = newCount;
    },

    // Ajouter un article au panier (création d'un objet Basket)
    async addToBasket(session) {
      const ticketCount = session.quantity || 0;

      if (ticketCount === 0) {
        Swal.fire({
          icon: "warning",
          title: "Attention",
          text: "Veuillez sélectionner une quantité valide de billets.",
        });
        return;
      }

      // Vérifier si l'utilisateur est connecté
      const token = localStorage.getItem("token");
      if (!token) {
        Swal.fire({
          icon: "error",
          title: "Non connecté",
          text: "Vous devez être connecté pour ajouter des séances à votre panier !",
        });
        return;
      }

      try {
        const API_URL = import.meta.env.VITE_API_URL;

        // Récupérer l'utilisateur connecté
        const userResponse = await axios.get(`${API_URL}/auth/user/`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!userResponse.data || !userResponse.data.id) {
          Swal.fire({
            icon: "error",
            title: "Erreur",
            text: "Problème lors de la récupération des informations utilisateur.",
          });
          return;
        }

        this.userId = userResponse.data.id;

        // Récupérer le panier pour voir si la séance y est déjà
        const basketResponse = await axios.get(`${API_URL}/basket/`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        const existingItem = basketResponse.data.find(
          (item) => item.session.id === session.id
        );

        if (existingItem) {
          // Mettre à jour la quantité avec PATCH
          await axios.patch(
            `${API_URL}/basket/${existingItem.id}/`,
            { quantity: existingItem.quantity + ticketCount },
            { headers: { Authorization: `Bearer ${token}` } }
          );
          Swal.fire({
            icon: "success",
            title: "Ajout au panier",
            text: "Quantité mise à jour dans le panier !",
          });
        } else {
          // Ajouter une nouvelle séance au panier avec POST
          await axios.post(
            `${API_URL}/basket/`,
            { session_id: session.id, quantity: ticketCount, user_id: this.userId },
            { headers: { Authorization: `Bearer ${token}` } }
          );
          Swal.fire({
            icon: "success",
            title: "Ajout réussi",
            text: "Article ajouté au panier !",
          });
        }
      } catch (error) {
        console.error("Erreur lors de l'ajout au panier:", error);
        Swal.fire({
          icon: "error",
          title: "Erreur",
          text: "Une erreur est survenue. Veuillez réessayer.",
        });
      }
    }
  }
};
</script>

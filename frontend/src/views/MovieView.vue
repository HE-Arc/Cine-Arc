<template>
  <div class="container mt-5">
    <div class="row">
      <!-- Left section for movie information -->
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

      <!-- Central section for synopsis and sessions -->
      <div class="col-md-8">
        <div v-if="movie" class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">Synopsis</h5>
            <p>{{ movie.synopsis }}</p>
          </div>
        </div>

        <!-- Available sessions -->
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
                    <!-- Input field to modify ticket quantity -->
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
      movie: null, // Stores the movie details
      sessions: [], // Stores all available sessions
      userId: null, // Stores the ID of the logged-in user
    };
  },
  async mounted() {
    try {
      const API_URL = import.meta.env.VITE_API_URL;

      // Fetch movie details based on the route parameter
      const movieResponse = await axios.get(`${API_URL}/movies/${this.$route.params.id}`);
      this.movie = movieResponse.data;

      // Fetch all sessions
      const sessionsResponse = await axios.get(`${API_URL}/sessions`);
      this.sessions = sessionsResponse.data;
    } catch (error) {
      // Handle errors during API calls
      Swal.fire({
        icon: "error",
        title: "Erreur",
        text: "Une erreur est survenue lors de la récupération des données.",
      });
    }
  },
  computed: {
    // Filter sessions to display only those related to the current movie and in the future
    filteredSessions() {
      if (!this.movie || !this.sessions) return [];

      return this.sessions
        .filter(session => {
          const sessionDate = new Date(session.date_hour);
          return session.movie && session.movie.id === this.movie.id && sessionDate >= new Date();
        })
        .map(session => {
          return {
            ...session,
            formattedDate: this.formatDate(session.date_hour) // Format session date
          };
        });
    }
  },
  methods: {
    // Format ISO date string into a readable French format
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

    // Get the current ticket count for a session
    getTicketsCount(session) {
      return session.quantity || 0;
    },

    // Update the ticket count for a session
    updateTicketCount(session, newCount) {
      newCount = parseInt(newCount, 10);
      if (isNaN(newCount) || newCount < 0) {
        newCount = 0;
      }
      if (newCount > session.room.capacity) {
        newCount = session.room.capacity; // Ensure the count does not exceed room capacity
      }

      session.quantity = newCount;
    },

    // Add a session to the basket
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

      // Check if the user is logged in
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

        // Fetch the logged-in user's details
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

        // Check if the session is already in the basket
        const basketResponse = await axios.get(`${API_URL}/basket/`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        const existingItem = basketResponse.data.find(
          (item) => item.session.id === session.id
        );

        if (existingItem) {
          // Update the quantity in the basket using PATCH
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
          // Add a new session to the basket using POST
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
        // Handle errors during the basket update process
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

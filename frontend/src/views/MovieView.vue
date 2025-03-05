<template>
  <div class="container mt-5">
    <!-- Conteneur principal pour la mise en page -->
    <div class="row">
      <!-- Encadré gauche pour les informations du film -->
      <div class="col-md-4">
        <div v-if="movie" class="card movie-card">
          <div class="card-body">
            <!-- Encadré pour l'image du film -->
            <div class="card mb-3">
              <img :src="movie.picture_url" :alt="movie.title" class="card-img-top movie-img" />
            </div>
            <h5 class="card-title">{{ movie.title }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ movie.release_date }}</h6>

            <p><strong>Duration :</strong> {{ movie.duration }} min</p>
            <p><strong>Type :</strong> {{ movie.type }}</p>
            <p><strong>Rating :</strong>  {{ movie.rating }} / 10 ⭐</p>
          </div>
        </div>
      </div>

      <!-- Conteneur central pour le synopsis et les séances -->
      <div class="col-md-8">
        <!-- Synopsis du film -->
        <div v-if="movie" class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">Synopsis</h5>
            <p>{{ movie.synopsis }}</p>
          </div>
        </div>

        <!-- Séances disponibles pour ce film -->
        <div class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">Séances disponibles</h5>
            <!-- Affichage des séances -->
            <div v-if="filteredSessions.length > 0">
              <ul class="list-group">
                <li v-for="session in filteredSessions" :key="session.id" class="list-group-item">
                  <strong>{{ session.formattedDate }}</strong> - {{ session.room.name }}
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

export default {
  data() {
    return {
      movie: null,
      sessions: [],
    };
  },
  async mounted() {
    try {
      // Récupérer les détails du film
      const movieResponse = await axios.get(`http://localhost:8000/api/movies/${this.$route.params.id}`);
      this.movie = movieResponse.data;

      // Récupérer toutes les séances
      const sessionsResponse = await axios.get("http://localhost:8000/api/sessions");
      this.sessions = sessionsResponse.data;
    } catch (error) {
      console.error("Error fetching movie or session details:", error);
    }
  },
  computed: {
    // Filtrer les séances pour n'afficher que celles correspondant au film actuel
    filteredSessions() {
      if (!this.movie) return [];

      return this.sessions
        .filter(session => session.movie.id === this.movie.id)
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
      
      // Obtenir la date au format "03 mars 2025"
      const formattedDate = date.toLocaleDateString("fr-FR", {
        day: "2-digit",
        month: "long",
        year: "numeric"
      });

      // Obtenir l'heure au format "19:57"
      const formattedTime = date.toLocaleTimeString("fr-FR", {
        hour: "2-digit",
        minute: "2-digit"
      });

      return `Le ${formattedDate} à ${formattedTime}`;
    }
  }
};
</script>

<style scoped>
.movie-card {
  max-width: 100%;
  margin: auto;
}

.movie-img {
  width: 100%;
  border-radius: 10px;
}

.card-body {
  padding: 20px;
}

.card-title {
  font-size: 1.25rem;
  font-weight: bold;
}

.card-subtitle {
  font-size: 1rem;
  color: #6c757d;
}

.list-group-item {
  font-size: 1rem;
}
</style>

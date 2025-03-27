<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">Films</h1>

    <!-- Affichage du spinner pendant le chargement -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="sr-only">Chargement...</span>
      </div>
      <p>Chargement des films...</p>
    </div>

    <!-- Affichage des films avec 4 colonnes fixes -->
    <div v-else-if="movies.length > 0" class="row row-cols-2 row-cols-md-4 g-3">
      <div v-for="movie in movies" :key="movie.id" class="col">
        <div class="card p-2" style="cursor: pointer;" @click="goToMovie(movie.id)">
          <img :src="movie.picture_url" :alt="movie.title" class="card-img-top movie-img" />
        </div>
      </div>
    </div>

    <!-- Si aucun film n'est disponible -->
    <div v-else class="text-center">
      <p>Aucun film disponible.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

const API_BASE_URL = import.meta.env.VITE_API_URL;

export default {
  data() {
    return {
      movies: [],
      loading: true,
    };
  },
  created() {
    this.fetchMovies();
  },
  methods: {
    async fetchMovies() {
      try {
        const response = await axios.get(`${API_BASE_URL}/movies/`);
        this.movies = response.data;
      } catch (error) {
        console.error("Error fetching movies:", error);
        Swal.fire({
          title: "Erreur !",
          text: "Impossible de récupérer les films. Veuillez réessayer plus tard.",
          icon: "error",
        });
      } finally {
        this.loading = false;
      }
    },
    goToMovie(id) {
      this.$router.push(`/movies/${id}`);
    },
  },
};
</script>

<style scoped>
.movie-img {
  width: 100%;
  object-fit: cover;
}

.card {
  transition: transform 0.3s ease;
}

.card:hover {
  transform: scale(1.05);
}
</style>

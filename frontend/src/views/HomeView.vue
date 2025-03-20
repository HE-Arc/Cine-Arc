<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">Movies</h1>

    <!-- Affichage du spinner pendant le chargement -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div>
      <p>Loading movies...</p>
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
      <p>No movies available.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

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
  object-fit: cover; /* 🔥 Assure un bon cadrage */
}

.card {
  transition: transform 0.3s ease;
}

.card:hover {
  transform: scale(1.05);
}
</style>

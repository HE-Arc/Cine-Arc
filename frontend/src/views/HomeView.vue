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

    <!-- Affichage des films si disponible -->
    <div v-else-if="movies.length > 0" class="row row-cols-1 row-cols-md-3 g-4">
      <div
        v-for="movie in movies"
        :key="movie.id"
        class="col"
      >
        <div class="card" style="cursor: pointer;" @click="goToMovie(movie.id)">
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
        const response = await axios.get("http://localhost:8000/api/movies/");
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
  height: 250px;
  object-fit: cover;
  width: 100%;
}

.card {
  transition: transform 0.3s ease;
}

.card:hover {
  transform: scale(1.05);
}
</style>

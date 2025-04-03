<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">Films</h1>

    <!-- Display spinner while loading -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Display movies in a grid with 4 fixed columns -->
    <div v-else-if="movies.length > 0" class="row row-cols-2 row-cols-md-4 g-3">
      <div v-for="movie in movies" :key="movie.id" class="col">
        <div class="card p-2" style="cursor: pointer;" @click="goToMovie(movie.id)">
          <img :src="movie.picture_url" :alt="movie.title" class="card-img-top movie-img" />
        </div>
      </div>
    </div>

    <!-- If no movies are available -->
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
      movies: [], // List of movies
      loading: true, // Loading state
    };
  },
  created() {
    this.fetchMovies(); // Fetch movies when the component is created
  },
  methods: {
    async fetchMovies() {
      try {
        const response = await axios.get(`${API_BASE_URL}/movies/`);
        this.movies = response.data; // Store the fetched movies
      } catch (error) {
        // Show an error alert if fetching movies fails
        Swal.fire({
          title: "Erreur !",
          text: "Impossible de récupérer les films. Veuillez réessayer plus tard.",
          icon: "error",
        });
      } finally {
        this.loading = false; // Set loading to false after the request
      }
    },
    goToMovie(id) {
      this.$router.push(`/movies/${id}`); // Navigate to the movie details page
    },
  },
};
</script>

<style scoped>
.movie-img {
  width: 100%; /* Ensure the image takes up the full width */
  object-fit: cover; /* Maintain aspect ratio and cover the container */
}

.card {
  transition: transform 0.3s ease; /* Smooth scaling effect on hover */
}

.card:hover {
  transform: scale(1.05); /* Slightly enlarge the card on hover */
}
</style>

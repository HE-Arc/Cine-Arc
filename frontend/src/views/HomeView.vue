<template>
  <div class="container mt-4">
    <!-- Titre + filtre alignés -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="mb-0">Films</h1>
      <div class="d-flex align-items-center">
        <label for="genreSelect" class="form-label me-2 mb-0">Filtrer par genre :</label>
        <select
          id="genreSelect"
          v-model="selectedType"
          class="form-select w-auto"
        >
          <option :value="null">Tous les genres</option>
          <option v-for="type in availableTypes" :key="type" :value="type">
            {{ type }}
          </option>
        </select>
      </div>
    </div>

    <!-- Loading spinner -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Grille de films -->
    <div v-else-if="filteredMovies.length > 0" class="row row-cols-2 row-cols-md-4 g-3">
      <div v-for="movie in filteredMovies" :key="movie.id" class="col">
        <div class="card p-2" style="cursor: pointer;" @click="goToMovie(movie.id)">
          <img :src="movie.picture_url" :alt="movie.title" class="card-img-top movie-img" />
        </div>
      </div>
    </div>

    <!-- Aucun film -->
    <div v-else class="text-center">
      <p>Aucun film disponible pour ce genre.</p>
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
      selectedType: null,
      loading: true,
    };
  },
  computed: {
  availableTypes() {
    const allTypes = this.movies.flatMap(movie =>
      movie.type ? movie.type.split(",").map(g => g.trim()) : []
    );
    return [...new Set(allTypes)].sort();
  },

  filteredMovies() {
    if (!this.selectedType) return this.movies;
    return this.movies.filter(movie =>
      movie.type && movie.type.split(",").map(g => g.trim()).includes(this.selectedType)
    );
  }

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
        Swal.fire({
          title: "Erreur !",
          text: "Impossible de récupérer les films.",
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
  height: 300px;
  object-fit: cover;
  border-radius: 10px;
}

.card {
  border-radius: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
}

.card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
</style>

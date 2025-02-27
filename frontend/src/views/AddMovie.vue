<template>
    <div class="container">
      <h1>Ajouter un Film</h1>
      <form @submit.prevent="addMovie">
        <label>Titre :</label>
        <input v-model="newMovie.title" type="text" required />
  
        <label>Synopsis :</label>
        <input v-model="newMovie.synopsis" type="text" required />
  
        <label>Durée (minutes) :</label>
        <input v-model="newMovie.duration" type="number" required />
  
        <label>Type :</label>
        <input v-model="newMovie.type" type="text" required />
  
        <label>Date de sortie :</label>
        <input v-model="newMovie.release_date" type="date" required />
  
        <label>URL de l'affiche :</label>
        <input v-model="newMovie.picture_url" type="text" required />
  
        <label>Note (1-10) :</label>
        <input v-model="newMovie.rating" type="number" min="1" max="10" required />
  
        <button type="submit" class="btn-submit">Ajouter</button>
        <button type="button" class="btn-cancel" @click="$router.push('/sessions')">Annuler</button>
      </form>
  
      <p v-if="movieErrors" class="error-message">{{ movieErrors }}</p>
    </div>
  </template>
  
  <script setup>
  import axios from "axios";
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  
  const router = useRouter();
  const movieErrors = ref(null);
  const newMovie = ref({
    title: "",
    synopsis: "",
    duration: "",
    type: "",
    release_date: "",
    picture_url: "",
    rating: 1,
  });
  
  // Ajouter un film via l'API
  const addMovie = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/movies/", newMovie.value);
      console.log("Film ajouté :", response.data);
  
      router.push("/sessions"); // Redirection vers la liste des séances après l'ajout
    } catch (error) {
      console.error("Erreur :", error);
      movieErrors.value = error.response?.data || "Erreur lors de l'ajout du film.";
    }
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
  }
  
  form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  label {
    font-weight: bold;
  }
  
  input {
    padding: 8px;
    font-size: 16px;
    border: 1px solid #ccc;
  }
  
  .btn-submit {
    background-color: #28a745;
    color: white;
    padding: 10px;
    border: none;
    cursor: pointer;
    font-size: 16px;
  }
  
  .btn-submit:hover {
    background-color: #218838;
  }
  
  .btn-cancel {
    background-color: #6c757d;
    color: white;
    padding: 10px;
    border: none;
    cursor: pointer;
    font-size: 16px;
  }
  
  .error-message {
    color: red;
    font-weight: bold;
  }
  </style>
  
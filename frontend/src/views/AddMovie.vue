<script setup>
import axios from "axios";
import { ref } from "vue";

const title = ref("");
const synopsis = ref("");
const type = ref("");
const release_date = ref("");
const picture_url = ref("");
const rating = ref("");
const duration = ref("");
const api_id = ref("");
const success = ref(false);
const errors = ref(null);

const submit = async () => {
  try {
    await axios.post("http://127.0.0.1:8000/api/movies/", {
      title: title.value,
      synopsis: synopsis.value,
      type: type.value,
      release_date: release_date.value,
      picture_url: picture_url.value,
      rating: parseFloat(rating.value), // Assure que c'est un nombre flottant
      duration: parseInt(duration.value, 10), // Convertit en entier
      api_id: parseInt(api_id.value, 10) // Convertit en entier
    });

    success.value = true;
    errors.value = null;
    resetForm();
  } catch (error) {
    errors.value = error.response?.data || "Erreur lors de l'ajout du film.";
    success.value = false;
  }
};

const resetForm = () => {
  title.value = "";
  synopsis.value = "";
  type.value = "";
  release_date.value = "";
  picture_url.value = "";
  rating.value = "";
  duration.value = "";
  api_id.value = "";
};
</script>

<template>
    <div class="container">
      <h1>Ajouter un Film</h1>
  
      <form @submit.prevent="submit">
        <label>Titre :</label>
        <input v-model="title" type="text" required />
  
        <label>Synopsis :</label>
        <textarea v-model="synopsis" required></textarea>
  
        <label>Type :</label>
        <input v-model="type" type="text" required />
  
        <label>Date de sortie :</label>
        <input v-model="release_date" type="date" required />
  
        <label>Image (URL) :</label>
        <input v-model="picture_url" type="url" required />
  
        <label>Note :</label>
        <input v-model="rating" type="number" step="0.1" min="0" max="10" required />
  
        <label>Durée (en minutes) :</label>
        <input v-model="duration" type="number" min="1" required />
  
        <label>ID API :</label>
        <input v-model="api_id" type="number" required />
  
        <button type="submit">Ajouter</button>
      </form>
  
      <p v-if="success" class="success">Film ajouté avec succès !</p>
      <p v-if="errors" class="error">{{ errors }}</p>
    </div>
  </template>
    

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
}

form {
  display: flex;
  flex-direction: column;
}

input, textarea, button {
  margin-top: 5px;
  padding: 8px;
}

.success {
  color: green;
}

.error {
  color: red;
}
</style>

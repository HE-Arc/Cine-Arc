<script setup>
import axios from "axios";
import { ref, onMounted, watch } from "vue";

const movies = ref([]);
const rooms = ref([]);
const sessions = ref([]);
const movieId = ref("");
const roomId = ref("");
const dateHour = ref("");
const success = ref(false);
const errors = ref(null);
const isEditing = ref(false);
const currentSessionId = ref(null);

// Charger les films, salles et séances
const fetchData = async () => {
  try {
    const moviesResponse = await axios.get("http://127.0.0.1:8000/api/movies/");
    movies.value = moviesResponse.data;

    const roomsResponse = await axios.get("http://127.0.0.1:8000/api/room/");
    rooms.value = roomsResponse.data;

    const sessionsResponse = await axios.get("http://127.0.0.1:8000/api/sessions/");
    sessions.value = sessionsResponse.data;
  } catch (error) {
    console.error("Erreur lors du chargement des films, salles ou séances:", error);
  }
};

onMounted(fetchData);

// Mettre automatiquement à jour `roomId` lorsque `movieId` change
watch(movieId, (newMovieId) => {
  const selectedMovie = movies.value.find(movie => movie.id === newMovieId);
  if (selectedMovie && selectedMovie.roomId) {
    roomId.value = selectedMovie.roomId; // Affecter la salle liée au film
  } else {
    roomId.value = ""; // Réinitialiser si aucun lien
  }
});

// Créer ou Modifier une séance
const submit = async () => {
  try {
    if (isEditing.value) {
      // Mettre à jour une séance existante
      await axios.put(`http://127.0.0.1:8000/api/sessions/${currentSessionId.value}/`, {
        movie_id: movieId.value,
        room_id: roomId.value,
        date_hour: dateHour.value,
      });
    } else {
      // Créer une nouvelle séance
      await axios.post("http://127.0.0.1:8000/api/sessions/", {
        movie_id: movieId.value,
        room_id: roomId.value,
        date_hour: dateHour.value,
      });
    }

    success.value = true;
    errors.value = null;
    isEditing.value = false;
    currentSessionId.value = null;
    fetchData(); // Recharger les séances après modification/ajout
  } catch (error) {
    errors.value = error.response?.data || "Une erreur est survenue.";
    success.value = false;
  }
};

// Préparer la modification d'une séance
const editSession = (session) => {
  movieId.value = session.movie.id;
  roomId.value = session.room.id;
  dateHour.value = session.date_hour;
  currentSessionId.value = session.id;
  isEditing.value = true;
};

// Supprimer une séance
const deleteSession = async (sessionId) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/sessions/${sessionId}/`);
    fetchData(); // Rafraîchir la liste après suppression
  } catch (error) {
    console.error("Erreur lors de la suppression :", error);
  }
};
</script>

<template>
  <div class="container">
    <h1>Gestion des Séances</h1>
    
    <!-- Formulaire pour ajouter/modifier une séance -->
    <form @submit.prevent="submit">
      <label>Film :</label>
      <select v-model="movieId">
        <option v-for="movie in movies" :key="movie.id" :value="movie.id">
          {{ movie.title }}
        </option>
      </select>

      <label>Salle :</label>
      <select v-model="roomId">
        <option v-for="room in rooms" :key="room.id" :value="room.id">
          {{ room.name }} (Capacité: {{ room.capacity }})
        </option>
      </select>

      <label>Date et Heure :</label>
      <input v-model="dateHour" type="datetime-local" />

      <button type="submit">{{ isEditing ? "Modifier la séance" : "Créer la séance" }}</button>
    </form>

    <p v-if="success" style="color: green;">Séance ajoutée/modifiée avec succès !</p>
    <p v-if="errors" style="color: red;">Erreur : {{ errors }}</p>

    <!-- Liste des séances avec boutons Modifier/Supprimer -->
    <h2>Liste des Séances</h2>
    <ul>
      <li v-for="session in sessions" :key="session.id">
        {{ session.movie.title }} - {{ session.room.name }} - {{ session.date_hour }}
        <button @click="editSession(session)">Modifier</button>
        <button @click="deleteSession(session.id)">Supprimer</button>
      </li>
    </ul>
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

label {
  margin-top: 10px;
}

input, select, button {
  margin-top: 5px;
  padding: 8px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background: #222;
  padding: 10px;
  margin: 5px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

button:hover {
  opacity: 0.8;
}
</style>

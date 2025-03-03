<script setup>
import axios from "axios";
import { ref, onMounted, watch, nextTick } from "vue";
import { useRouter } from "vue-router"; // Importation du router

const router = useRouter(); // Initialisation du router

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
const formRef = ref(null); // Référence au formulaire

// Charger les films, salles et séances
const fetchData = async () => {
  try {
    const [moviesResponse, roomsResponse, sessionsResponse] = await Promise.all([
      axios.get("http://127.0.0.1:8000/api/movies/"),
      axios.get("http://127.0.0.1:8000/api/room/"),
      axios.get("http://127.0.0.1:8000/api/sessions/"),
    ]);

    console.log("Sessions fetched:", sessionsResponse.data); // 🔍 Vérifie ce qui est récupéré
    movies.value = moviesResponse.data;
    rooms.value = roomsResponse.data;
    sessions.value = sessionsResponse.data;
  } catch (error) {
    errors.value = "Erreur lors du chargement des données.";
    console.error(error);
  }
};

//Pour quand l'api sera mise en place
// const fetchData = async () => {
//   try {
//     const API_KEY = "CLE DE L'API DE TMBD ICI"; qui est dans un fichier .env 
//     const moviesResponse = await axios.get(
//       `https://api.themoviedb.org/3/movie/popular?api_key=${API_KEY}&language=fr-FR`
//     );

//     movies.value = moviesResponse.data.results; 

//     const [roomsResponse, sessionsResponse] = await Promise.all([
//       axios.get("http://127.0.0.1:8000/api/room/"),
//       axios.get("http://127.0.0.1:8000/api/sessions/"),
//     ]);

//     rooms.value = roomsResponse.data;
//     sessions.value = sessionsResponse.data;
//   } catch (error) {
//     errors.value = "Erreur lors du chargement des données.";
//     console.error(error);
//   }
// };

onMounted(fetchData);

// Mettre automatiquement à jour `roomId` lorsque `movieId` change
watch(movieId, (newMovieId) => {
  const selectedMovie = movies.value.find(movie => movie.id === newMovieId);
  roomId.value = selectedMovie?.roomId || "";
});

// Formater la date pour éviter le "Z" (UTC)
const formatDate = (isoString) => {
  if (!isoString) return "";
  const date = new Date(isoString);
  return date.toLocaleString("fr-FR", {
    dateStyle: "long",
    timeStyle: "short"
  });
};

// Créer ou Modifier une séance
const submit = async () => {
  try {
    const payload = {
      movie_id: movieId.value,
      room_id: roomId.value,
      date_hour: dateHour.value,
    };

    if (isEditing.value) {
      await axios.put(`http://127.0.0.1:8000/api/sessions/${currentSessionId.value}/`, payload);
    } else {
      await axios.post("http://127.0.0.1:8000/api/sessions/", payload);
    }

    success.value = true;
    errors.value = null;
    resetForm();
    fetchData();
  } catch (error) {
    errors.value = error.response?.data || "Une erreur est survenue.";
    success.value = false;
  }
};

// Réinitialiser le formulaire
const resetForm = () => {
  movieId.value = "";
  roomId.value = "";
  dateHour.value = "";
  isEditing.value = false;
  currentSessionId.value = null;
};

// Modifier une séance et faire défiler la page vers le formulaire
const editSession = (session) => {
  isEditing.value = true;
  currentSessionId.value = session.id;

  // Pré-remplir les champs du formulaire
  movieId.value = session.movie.id;
  
  // Met à jour la salle et force Vue à rafraîchir l'affichage
  roomId.value = session.room.id;
  nextTick(() => {
    roomId.value = session.room.id; // Assure que Vue le met bien à jour
  });

  // Corrige la date pour `datetime-local`
  dateHour.value = new Date(session.date_hour).toISOString().slice(0, 16);

  //Fait défiler vers le formulaire
  nextTick(() => {
    formRef.value.scrollIntoView({ behavior: "smooth", block: "start" });
  });
};

  // Remonter au formulaire
  nextTick(() => {
    formRef.value.scrollIntoView({ behavior: "smooth", block: "start" });
  });

// Supprimer une séance
const deleteSession = async (sessionId) => {
  if (!confirm("Voulez-vous vraiment supprimer cette séance ?")) return;

  try {
    await axios.delete(`http://127.0.0.1:8000/api/sessions/${sessionId}/`);
    fetchData();
  } catch (error) {
    errors.value = "Erreur lors de la suppression.";
  }
};

</script>

<template>
  <div class="container">
    <h1>Séances</h1>

    <form ref="formRef" @submit.prevent="submit">
      <label>Film :</label>
      <select v-model="movieId" required>
        <option value="" disabled>Sélectionnez un film</option>
        <option v-for="movie in movies" :key="movie.id" :value="movie.id">
          {{ movie.title }}
        </option>
      </select>

      <label>Salle :</label>
      <select v-model="roomId" required>
        <option value="" disabled>Sélectionnez une salle</option>
        <option v-for="room in rooms" :key="room.id" :value="room.id">
          {{ room.name }} (Capacité: {{ room.capacity }})
        </option>
      </select>

      <label>Date et Heure :</label>
      <input v-model="dateHour" type="datetime-local" required />

      <button :class="isEditing ? 'edit-btn' : 'create-btn'" type="submit">
        {{ isEditing ? "Modifier" : "Créer une séance" }}
      </button>
    </form>

    <p v-if="success" class="success">Séance enregistrée avec succès !</p>
    <p v-if="errors" class="error">{{ errors }}</p>

    <h2>Liste des Séances</h2>
    <ul>
      <li v-for="session in sessions" :key="session.id">
        <div class="session-item">
          <img 
            v-if="session.movie.picture_url" 
            :src="session.movie.picture_url" 
            alt="Affiche du film" 
            class="movie-thumb"
          />
          <div class="session-details">
            <strong>{{ session.movie.title }}</strong> - 
            {{ session.room.name }} - 
            {{ formatDate(session.date_hour) }}
          </div>
        </div>
        <div class="session-actions">
          <button class="edit-btn" @click="editSession(session)">Modifier</button>
          <button class="delete-btn" @click="deleteSession(session.id)">Supprimer</button>
        </div>
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
  border-radius: 8px;
}

.session-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.movie-thumb {
  width: 60px;  /* Un peu plus grand pour mieux voir l'affiche */
  height: 90px;
}

.session-details {
  color: white !important;
  flex: 1;
}

.session-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

button {
  width: 100%; /*Tous les boutons prennent toute la largeur */
  padding: 10px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  color: white;
  text-align: center;
  display: block; /* Empêche les petits écarts de taille */
}

button:hover {
  opacity: 0.8;
}

/* Bouton "Créer" en vert */
.create-btn {
  background-color: #28a745;
}

.create-btn:hover {
  background-color: #218838;
}

/* Bouton "Ajouter un Film" en bleu */
.add-movie-btn {
  background-color: #007bff;
  margin-top: 10px;
}

.add-movie-btn:hover {
  background-color: #0056b3;
}

/* Bouton Modifier en Orange */
.edit-btn {
  background-color: #ff9800;
}

.edit-btn:hover {
  background-color: #e68900;
}

/* Bouton Supprimer en Rouge */
.delete-btn {
  background-color: #d32f2f;
}

.delete-btn:hover {
  background-color: #b71c1c;
}

.success {
  color: green;
}

.error {
  color: red;
}
</style>

<script setup>
import axios from "axios";
import { ref, onMounted, watch, nextTick } from "vue";

// Replace with the API URL from environment variables
const API_BASE_URL = import.meta.env.VITE_API_URL;

// Reactive variables for movies, rooms, sessions, and form inputs
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
const formRef = ref(null); // Reference to the form element

// Fetch movies, rooms, and sessions data from the API
const fetchData = async () => {
  try {
    const [moviesResponse, roomsResponse, sessionsResponse] = await Promise.all([
      axios.get(`${API_BASE_URL}/movies/`),
      axios.get(`${API_BASE_URL}/room/`),
      axios.get(`${API_BASE_URL}/sessions/`),
    ]);

    // Filter sessions to only include future sessions
    movies.value = moviesResponse.data;
    rooms.value = roomsResponse.data;

    sessions.value = sessionsResponse.data.filter(session => {
      const sessionDate = new Date(session.date_hour);
      return sessionDate >= new Date(); // Compare with the current date
    });
  } catch (error) {
    errors.value = "Erreur lors du chargement des données."; // Error message for data loading
  }
};

// Fetch data when the component is mounted
onMounted(fetchData);

// Automatically update `roomId` when `movieId` changes
watch(movieId, (newMovieId) => {
  const selectedMovie = movies.value.find(movie => movie.id === newMovieId);
  roomId.value = selectedMovie?.roomId || "";
});

// Format the date to avoid the "Z" (UTC) suffix
const formatDate = (isoString) => {
  if (!isoString) return "";
  const date = new Date(isoString);
  return date.toLocaleString("fr-FR", {
    dateStyle: "long",
    timeStyle: "short"
  });
};

// Create or update a session
const submit = async () => {
  try {
    const payload = {
      movie_id: movieId.value,
      room_id: roomId.value,
      date_hour: dateHour.value,
    };

    if (isEditing.value) {
      // Update an existing session
      await axios.put(`${API_BASE_URL}/sessions/${currentSessionId.value}/`, payload);
    } else {
      // Create a new session
      await axios.post(`${API_BASE_URL}/sessions/`, payload);
    }

    success.value = true; // Indicate success
    errors.value = null; // Clear errors
    resetForm(); // Reset the form
    fetchData(); // Refresh the data
  } catch (error) {
    errors.value = error.response?.data || "Une erreur est survenue."; // Display error message
    success.value = false; // Indicate failure
  }
};

// Reset the form fields
const resetForm = () => {
  movieId.value = "";
  roomId.value = "";
  dateHour.value = "";
  isEditing.value = false;
  currentSessionId.value = null;
};

// Edit a session and scroll to the form
const editSession = (session) => {
  isEditing.value = true; // Set editing mode
  currentSessionId.value = session.id; // Set the current session ID

  // Pre-fill the form fields
  movieId.value = session.movie.id;

  // Update the room and force Vue to refresh the display
  roomId.value = session.room.id;
  nextTick(() => {
    roomId.value = session.room.id; // Ensure Vue updates it
  });

  // Adjust the date for `datetime-local` input
  const sessionDate = new Date(session.date_hour);
  const localDate = new Date(sessionDate.getTime() - sessionDate.getTimezoneOffset() * 60000);
  dateHour.value = localDate.toISOString().slice(0, 16);

  // Scroll to the form
  nextTick(() => {
    formRef.value.scrollIntoView({ behavior: "smooth", block: "start" });
  });
};

// Delete a session
const deleteSession = async (sessionId) => {
  if (!confirm("Voulez-vous vraiment supprimer cette séance ?")) return; // Confirm deletion

  try {
    await axios.delete(`${API_BASE_URL}/sessions/${sessionId}/`); // Delete the session
    fetchData(); // Refresh the data
  } catch {
    errors.value = "Erreur lors de la suppression."; // Error message for deletion
  }
};

</script>

<template>
  <div class="container">
    <h1>Séances</h1>

    <!-- Form for creating or editing a session -->
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

    <!-- Success and error messages -->
    <p v-if="success" class="success">Séance enregistrée avec succès !</p>
    <p v-if="errors" class="error">{{ errors }}</p>

    <!-- List of sessions -->
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
  width: 60px;  /* Slightly larger for better visibility */
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
  width: 100%; /* All buttons take full width */
  padding: 10px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  color: white;
  text-align: center;
  display: block; /* Prevent small size discrepancies */
}

button:hover {
  opacity: 0.8;
}

/* "Create" button in green */
.create-btn {
  background-color: #28a745;
}

.create-btn:hover {
  background-color: #218838;
}

/* "Add Movie" button in blue */
.add-movie-btn {
  background-color: #007bff;
  margin-top: 10px;
}

.add-movie-btn:hover {
  background-color: #0056b3;
}

/* Edit button in orange */
.edit-btn {
  background-color: #ff9800;
}

.edit-btn:hover {
  background-color: #e68900;
}

/* Delete button in red */
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

<script setup>
import axios from "axios";
import { ref, nextTick } from "vue";
import { useRouter } from "vue-router"; // Importation du router Vue

const router = useRouter(); // Accès au router

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
const formRef = ref(null); // Référence au formulaire

const submit = async () => {
  try {
    await axios.post("http://127.0.0.1:8000/api/movies/", {
      title: title.value,
      synopsis: synopsis.value,
      type: type.value,
      release_date: release_date.value,
      picture_url: picture_url.value,
      rating: parseFloat(rating.value),
      duration: parseInt(duration.value, 10),
      api_id: parseInt(api_id.value, 10),
    });

    success.value = true;
    errors.value = null;
    resetForm();

    // Faire défiler vers le formulaire après ajout
    nextTick(() => {
      formRef.value.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  } catch (error) {
    errors.value = error.response?.data || "Erreur lors de l'ajout du film.";
    success.value = false;
  }
};

// Réinitialiser le formulaire
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

// Rediriger vers la page des séances
const goToSessions = () => {
  router.push("/sessions");
};
</script>

<template>
  <div class="container">
    <h1>Ajouter un Film</h1>

    <div class="card">
      <form ref="formRef" @submit.prevent="submit">
        <div class="form-grid">
          <div class="input-group">
            <label>Titre</label>
            <input v-model="title" type="text" required />
          </div>

          <div class="input-group">
            <label>Type</label>
            <input v-model="type" type="text" required />
          </div>

          <div class="input-group">
            <label>Date de sortie</label>
            <input v-model="release_date" type="date" required />
          </div>

          <div class="input-group">
            <label>Durée (min)</label>
            <input v-model="duration" type="number" min="1" required />
          </div>

          <div class="input-group full-width">
            <label>Synopsis</label>
            <textarea v-model="synopsis" rows="2" required></textarea>
          </div>

          <div class="input-group">
            <label>Note</label>
            <input v-model="rating" type="number" step="0.1" min="0" max="10" required />
          </div>

          <div class="input-group">
            <label>ID API</label>
            <input v-model="api_id" type="number" required />
          </div>

          <div class="input-group">
            <label>Image (URL)</label>
            <input v-model="picture_url" type="url" required />
          </div>
        </div>

        <button class="create-btn" type="submit">Ajouter</button>
      </form>

      <!-- Bouton Afficher les Séances -->
      <button class="sessions-btn" @click="goToSessions">Afficher les Séances</button>
    </div>

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

.card {
  background: #222;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(97, 3, 3, 0.1);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group label {
  font-weight: bold;
  margin-bottom: 5px;
}

.input-group input,
.input-group textarea {
  padding: 8px;
  border: 1px solid #1a1515;
  border-radius: 5px;
  font-size: 14px;
}

.full-width {
  grid-column: span 2;
}

button {
  margin-top: 10px;
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  color: white;
}

/* Bouton Ajouter en Vert */
.create-btn {
  background-color: #28a745;
}

.create-btn:hover {
  background-color: #218838;
}

/* Bouton Afficher les Séances en Bleu */
.sessions-btn {
  background-color: #007bff;
  margin-top: 15px;
}

.sessions-btn:hover {
  background-color: #0056b3;
}

.success {
  color: green;
  font-weight: bold;
  text-align: center;
  margin-top: 10px;
}

.error {
  color: red;
  font-weight: bold;
  text-align: center;
  margin-top: 10px;
}

/* Responsive */
@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .full-width {
    grid-column: span 1;
  }
}
</style>

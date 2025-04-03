<template>
    <div class="container mt-5 text-center">
        <h2>✅ Paiement Réussi !</h2>
        <p>Votre paiement a été confirmé et vos billets sont maintenant réservés.</p>
        <router-link to="/" class="btn btn-primary">Retour à l'accueil</router-link>
    </div>
</template>

<script setup>
import { onMounted } from "vue";
import axios from "axios";

onMounted(async () => {
    try {
        const API_URL = import.meta.env.VITE_API_URL;
        // Récupération de l'utilisateur connecté
        const userResponse = await axios.get(`${API_URL}/auth/user/`, {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });

        console.log("Utilisateur connecté :", userResponse.data);

        // Mise à jour du panier après le paiement
        const response = await axios.post(
            `${API_URL}/payment/success/`,
            {},  // Ajouter un objet vide dans la requête `POST`
            {
                headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
            }
        );

        console.log("Mise à jour du panier :", response.data);
    } catch (error) {
        console.error("Erreur mise à jour du panier :", error);
    }
});
</script>

<style scoped>
.container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
}
</style>

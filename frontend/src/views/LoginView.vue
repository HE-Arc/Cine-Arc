<template>
    <div class="container">
        <h2>Connexion</h2>
        <form @submit.prevent="login">
        <div class="form-group">
            <label>Email</label>
            <input v-model="email" type="email" class="form-control" required />
        </div>

        <div class="form-group">
            <label>Mot de passe</label>
            <input v-model="password" type="password" class="form-control" required />
        </div>

        <button type="submit" class="btn btn-success">Se connecter</button>
        <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
        </form>

        <!-- Bouton "Créer un compte" -->
        <p class="mt-3">
        Pas encore de compte ? <router-link to="/register">Créer un compte</router-link>
        </p>
    </div>
</template>

<script>
import axios from "axios";
import { useRouter } from "vue-router";
import { ref } from "vue";
import Swal from "sweetalert2";

export default {
    setup() {
        const router = useRouter();
        const email = ref("");
        const password = ref("");
        const errorMessage = ref("");

        const login = async () => {
        try {
            const API_URL = import.meta.env.VITE_API_URL;
            const response = await axios.post(`${API_URL}/auth/login/`, {
            email: email.value,
            password: password.value,
            });

            localStorage.setItem("token", response.data.access);
            axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.access}`;

            Swal.fire({
                title: "Connexion réussie !",
                text: "Bienvenue, vous allez être redirigé.",
                icon: "success",
                timer: 2000,
                showConfirmButton: false,
            });
            setTimeout(() => {
                router.push("/").then(() => {
                    location.reload();
                });
            }, 2000);
        } catch (error) {
            errorMessage.value = "Email ou mot de passe incorrect.";
            console.error(error);
            if (error.response && error.response.status === 401) {
            Swal.fire({
                title: "Échec de la connexion",
                text: "Email ou mot de passe incorrect.",
                icon: "error",
            });
            } else {
            Swal.fire({
                title: "Erreur serveur",
                text: "Un problème est survenu, veuillez réessayer plus tard.",
                icon: "error",
            });
            }
        }
        };

        return { email, password, login, errorMessage };
    },
};
</script>

<style scoped>
.container {
    max-width: 400px;
    margin: auto;
    padding: 20px;
}
</style>
  
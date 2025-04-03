import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from "./store";

// Importer Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js'


// Vérification du token expiré
const token = localStorage.getItem("token")
if (token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const isExpired = payload.exp * 1000 < Date.now()

    if (isExpired) {
      console.warn("Token expiré, déconnexion automatique")
      store.dispatch("logout")  // Appelle le logout de Vuex
    }
  } catch (e) {
    console.error("Erreur de parsing du token", e)
    store.dispatch("logout")
  }
}

// Créer l'application Vue
const app = createApp(App)

// Utiliser le store et le routeur (si vous en avez)
app.use(store);
app.use(router)

// Monter l'application sur l'élément avec id 'app'
app.mount('#app')

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from "./store";

// Importer Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css';

// Créer l'application Vue
const app = createApp(App)

// Utiliser le store et le routeur (si vous en avez)
app.use(store);
app.use(router)

// Monter l'application sur l'élément avec id 'app'
app.mount('#app')

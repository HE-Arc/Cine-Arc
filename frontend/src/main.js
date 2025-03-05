import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Importer Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css';

// Créer l'application Vue
const app = createApp(App)

// Utiliser le routeur (si vous en avez un)
app.use(router)

// Monter l'application sur l'élément avec id 'app'
app.mount('#app')

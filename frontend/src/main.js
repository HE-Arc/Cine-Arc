import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from "./store"

// Import Bootstrap CSS and JS for styling and components
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Check if a token exists in localStorage
const token = localStorage.getItem("token")
if (token) {
  try {
    // Decode the token payload and check if it is expired
    const payload = JSON.parse(atob(token.split('.')[1]))
    const isExpired = payload.exp * 1000 < Date.now()

    if (isExpired) {
      console.warn("Token expired, performing automatic logout")
      store.dispatch("logout")  // Trigger Vuex logout action
    }
  } catch (e) {
    // Handle token parsing errors and perform logout
    console.error("Error parsing the token", e)
    store.dispatch("logout")
  }
}

// Create the Vue application instance
const app = createApp(App)

// Use Vuex store and Vue Router in the application
app.use(store)
app.use(router)

// Mount the Vue application to the DOM element with id 'app'
app.mount('#app')

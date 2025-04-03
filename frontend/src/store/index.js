import { createStore } from "vuex";
import axios from "axios";
import router from "@/router";

// Vuex store definition
const store = createStore({
  state: {
    // State to store user information
    user: null,
    // Token for authentication, retrieved from localStorage if available
    token: localStorage.getItem("token") || "",
    // Refresh token, retrieved from localStorage if available
    refreshToken: localStorage.getItem("refresh_token") || "",
  },
  mutations: {
    // Mutation to set the user information in the state
    setUser(state, user) {
      state.user = user;
    },
    // Mutation to set the authentication token in the state and localStorage
    setToken(state, token) {
      state.token = token;
      localStorage.setItem("token", token);
    },
    // Mutation to set the refresh token in the state and localStorage
    setRefreshToken(state, token) {
      state.refreshToken = token;
      localStorage.setItem("refresh_token", token);
    },
    // Mutation to clear user and token information during logout
    logout(state) {
      state.user = null;
      state.token = "";
      state.refreshToken = "";
      localStorage.removeItem("token");
      localStorage.removeItem("refresh_token");
    },
  },
  actions: {
    // Action to handle user login
    async login({ commit }, credentials) {
      try {
        const API_URL = import.meta.env.VITE_API_URL; // API base URL from environment variables
        const response = await axios.post(`${API_URL}/auth/login/`, credentials); // Send login request
        commit("setToken", response.data.access); // Store access token
        commit("setRefreshToken", response.data.refresh); // Store refresh token
        commit("setUser", { id: response.data.user_id, username: response.data.username }); // Store user information
        return true; // Indicate successful login
      } catch (error) {
        return false; // Indicate failed login
      }
    },
    // Action to fetch user information using the stored token
    async fetchUser({ commit, state }) {
      if (state.token) {
        try {
          const API_URL = import.meta.env.VITE_API_URL; // API base URL from environment variables
          const response = await axios.get(`${API_URL}/auth/user/`, {
            headers: { Authorization: `Bearer ${state.token}` }, // Include token in request headers
          });
          commit("setUser", response.data); // Update user information in the state
        } catch (error) {
          // Handle error silently
        }
      }
    },
    // Action to handle user logout
    logout({ commit }) {
      commit("logout"); // Clear user and token information
      router.push("/login"); // Redirect to login page
    },
  },
});

// Axios interceptor to handle token refresh
axios.interceptors.response.use(
  response => response, // Pass through successful responses
  async error => {
    const originalRequest = error.config; // Store the original request
    const isTokenExpired = error.response?.data?.code === "token_not_valid"; // Check if the token is expired
    const refresh = localStorage.getItem("refresh_token"); // Retrieve refresh token from localStorage

    if (isTokenExpired && refresh && !originalRequest._retry) {
      originalRequest._retry = true; // Mark the request as retried
      try {
        const API_URL = import.meta.env.VITE_API_URL; // API base URL from environment variables
        const res = await axios.post(`${API_URL}/auth/refresh/`, { refresh }); // Request a new access token
        const newAccess = res.data.access; // Extract the new access token

        store.commit("setToken", newAccess); // Update the token in the store
        originalRequest.headers["Authorization"] = `Bearer ${newAccess}`; // Update the authorization header
        return axios(originalRequest); // Retry the original request with the new token
      } catch (refreshError) {
        store.dispatch("logout"); // Logout the user if token refresh fails
        return Promise.reject(refreshError); // Reject the promise with the refresh error
      }
    }

    return Promise.reject(error); // Reject the promise with the original error
  }
);

export default store;

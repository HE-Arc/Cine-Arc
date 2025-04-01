import { createStore } from "vuex";
import axios from "axios";
import router from "@/router";

const store = createStore({
  state: {
    user: null,
    token: localStorage.getItem("token") || "",
    refreshToken: localStorage.getItem("refresh_token") || "",
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
      localStorage.setItem("token", token);
    },
    setRefreshToken(state, token) {
      state.refreshToken = token;
      localStorage.setItem("refresh_token", token);
    },
    logout(state) {
      state.user = null;
      state.token = "";
      state.refreshToken = "";
      localStorage.removeItem("token");
      localStorage.removeItem("refresh_token");
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const API_URL = import.meta.env.VITE_API_URL;
        const response = await axios.post(`${API_URL}/auth/login/`, credentials);
        commit("setToken", response.data.access);
        commit("setRefreshToken", response.data.refresh);
        commit("setUser", { id: response.data.user_id, username: response.data.username });
        return true;
      } catch (error) {
        console.error("Erreur de connexion :", error);
        return false;
      }
    },
    async fetchUser({ commit, state }) {
      if (state.token) {
        try {
          const API_URL = import.meta.env.VITE_API_URL;
          const response = await axios.get(`${API_URL}/auth/user/`, {
            headers: { Authorization: `Bearer ${state.token}` },
          });
          commit("setUser", response.data);
        } catch (error) {
          console.error("Erreur récupération user :", error);
        }
      }
    },
    logout({ commit }) {
      commit("logout");
      router.push("/login");
    },
  },
});

// Interceptor pour rafraîchir le token
axios.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    const isTokenExpired = error.response?.data?.code === "token_not_valid";
    const refresh = localStorage.getItem("refresh_token");

    if (isTokenExpired && refresh && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const API_URL = import.meta.env.VITE_API_URL;
        const res = await axios.post(`${API_URL}/auth/refresh/`, { refresh });
        const newAccess = res.data.access;

        store.commit("setToken", newAccess);
        originalRequest.headers["Authorization"] = `Bearer ${newAccess}`;
        return axios(originalRequest);
      } catch (refreshError) {
        store.dispatch("logout");
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default store;
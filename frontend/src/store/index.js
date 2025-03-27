import { createStore } from "vuex";
import axios from "axios";

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem("token") || "",
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
      localStorage.setItem("token", token);
    },
    logout(state) {
      state.user = null;
      state.token = "";
      localStorage.removeItem("token");
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const API_URL = import.meta.env.VITE_API_URL;
        const response = await axios.post(`${API_URL}/auth/login/`, credentials);
        commit("setToken", response.data.access);
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
    },
  },
});

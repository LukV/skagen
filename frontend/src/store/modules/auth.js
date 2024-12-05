// store/modules/auth.js
import axios from 'axios';
import apiClient from '@/apiClient';

const state = {
  accessToken: localStorage.getItem('accessToken') || null,
  refreshToken: localStorage.getItem('refreshToken') || null,
  authStatus: 'pending', // 'pending', 'authenticated', 'unauthenticated'
};

const mutations = {
  SET_TOKENS(state, tokens) {
    state.accessToken = tokens.access_token;
    state.refreshToken = tokens.refresh_token;
    localStorage.setItem('accessToken', tokens.access_token);
    localStorage.setItem('refreshToken', tokens.refresh_token);
    state.authStatus = 'authenticated';
  },
  CLEAR_AUTH(state) {
    state.accessToken = null;
    state.refreshToken = null;
    state.authStatus = 'unauthenticated';
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },
};

const actions = {
  async login({ commit }, credentials) {
    try {
      const response = await axios.post('/auth/login', credentials);
      commit('SET_TOKENS', response.data);
      // Fetch user data after login
      await this.dispatch('user/fetchUser');
    } catch (error) {
      throw error.response?.data?.detail || {
        code: "GENERIC_ERROR",
        message: "An error occurred. Please try again.",
        msgtype: "error",
      };
    }
  },
  logout({ commit }) {
    commit('CLEAR_AUTH');
    this.commit('user/CLEAR_USER');
  },
  async restoreAuth({ commit, state }) {
    if (state.accessToken) {
      try {
        await this.dispatch('user/fetchUser');
      } catch (error) {
        commit('CLEAR_AUTH');
      }
    } else {
      commit('CLEAR_AUTH');
    }
  },
};

const getters = {
  isAuthenticated: (state) => state.authStatus === 'authenticated',
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};

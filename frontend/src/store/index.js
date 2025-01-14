import { createStore } from 'vuex';
import axios from 'axios';
import apiClient from '@/utils/apiClient';

export default createStore({
    state: {
        user: null,
        accessToken: localStorage.getItem('accessToken') || null,
        refreshToken: localStorage.getItem('refreshToken') || null,
        authStatus: 'pending', // 'pending', 'authenticated', 'unauthenticated'
    },
    mutations: {
        SET_USER(state, user) {
            state.user = user;
            state.authStatus = 'authenticated';
        },
        SET_TOKENS(state, tokens) {
            state.accessToken = tokens.access_token;
            state.refreshToken = tokens.refresh_token;
            localStorage.setItem('accessToken', tokens.access_token);
            localStorage.setItem('refreshToken', tokens.refresh_token);
        },
        CLEAR_AUTH(state) {
            state.user = null;
            state.accessToken = null;
            state.refreshToken = null;
            state.authStatus = 'unauthenticated';
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
        },
    },
    actions: {
        async restoreAuth({ commit }) {
            if (localStorage.getItem('accessToken')) {
                try {
                    const userResponse = await apiClient.get('/users/me');
                    commit('SET_USER', userResponse.data);
                } catch (error) {
                    console.error("Failed to restore user session", error);
                    commit('CLEAR_AUTH');
                }
            } else {
                commit('CLEAR_AUTH');
            }
        },
        fetchUser({ commit }, user) {
            commit('SET_USER', user);
        },
        clearUser({ commit }) {
            commit('CLEAR_USER');
        },
        async login({ commit }, credentials) {
            try {
                const response = await axios.post('/auth/login', credentials);
                commit('SET_TOKENS', response.data);

                // Fetch user data using the access token
                const userResponse = await apiClient.get('/users/me');
                commit('SET_USER', userResponse.data);
            } catch (error) {
                const detail = error.response?.data?.detail;
                if (detail) {
                    throw detail;
                } else {
                    throw { code: "GENERIC_ERROR", message: "An error occurred. Please try again.", msgtype: "error" };
                }
            }
        },
        logout({ commit }) {
            commit('CLEAR_AUTH');
        },
    },
    getters: {
        isAuthenticated: (state) => state.authStatus === 'authenticated',
        getUser: (state) => state.user,
    },
});
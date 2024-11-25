import { createStore } from 'vuex';

export default createStore({
    state: {
        message: 'Hello, Vuex!',
    },
    getters: {
        message: (state) => state.message,
    },
    mutations: {
        setMessage(state, newMessage) {
            state.message = newMessage;
        },
    },
    actions: {
        updateMessage({ commit }, newMessage) {
            commit('setMessage', newMessage);
        },
    },
});

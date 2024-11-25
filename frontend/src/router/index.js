import { createRouter, createWebHistory } from 'vue-router';
import DefaultLayout from '@/layouts/DefaultLayout.vue';
import AuthLayout from '@/layouts/AuthLayout.vue';
import HomePage from '@/pages/HomePage.vue';
import LoginPage from '@/pages/LoginPage.vue';
import NotFoundPage from '@/pages/NotFoundPage.vue'; 

const routes = [
    {
        path: '/',
        component: DefaultLayout,
        children: [
            { path: '', name: 'Home', component: HomePage },
            { path: 'home', name: 'HomeAlias', component: HomePage }, 
        ],
    },
    {
        path: '/login',
        component: AuthLayout,
        children: [
            { path: '', name: 'Login', component: LoginPage },
        ],
    },
    {
        path: '/:pathMatch(.*)*', 
        name: 'NotFound',
        component: NotFoundPage,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;

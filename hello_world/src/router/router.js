import { createRouter, createWebHistory } from 'vue-router'
import LoginForm from "../views/LoginForm.vue";

const routes = [
    {
        path: '/login',
        name: 'login',
        component: LoginForm
    },
    {
        path: '/signup',
        name: 'signup',
        // component: SignIp
    },
    {
        path: '/reset',
        name: 'reset',
        // component: ResetPassword
    },
    {
        path: '/home',
        name: 'home',
        // component: Home
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;
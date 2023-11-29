import { createRouter, createWebHistory } from 'vue-router'
import LoginForm from "../views/LoginForm.vue";
import HomePage from "../views/HomePage.vue";
import ImageEdit from "@/views/ImageEdit.vue";

const routes = [
    {
        path: '/',
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
        component: HomePage
    },
    {
        path: '/edit',
        name: 'edit',
        component: ImageEdit
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;
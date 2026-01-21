// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import MovieQA from '@/components/MovieQA.vue'
import Moviestype from '@/views/Moviestype.vue'
import index from '@/views/index.vue'
const routes = [
    {
    path: '/',
    name: 'index',
    component: index
  },
  {
    path: '/movieqa',
    name: 'MovieQA',
    component: MovieQA
  },
  {
    path: '/list',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/movies_type',
    name: 'movies_type',
    component: Moviestype
  }
  
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
// /src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from "@/views/Login/Login.vue"
import Layout from "@/views/Layout/index.vue"
import Register from "@/views/Register/Register.vue"
import ForgetPassword from "@/views/ForgetPassword.vue"
import ChartsPage from "@/views/ChartsPage/ChartsPage.vue"
import GraphVis from "@/views/Graph/GraphVisualization.vue"
import Opinion from "@/views/Sentiment/index.vue"
import Usertext from "@/views/UserText/index.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/forget',
      component: ForgetPassword
    },
    {
      path: '/register',
      component: Register
    },
    {
      path: '/charts',
      component: ChartsPage
    },
    {
      path: '/graphvisual',
      component: GraphVis
    },
    {
      path: '/opinion',
      component: Opinion
    },
    {
      path: '/text',
      component: Usertext
    },
  ],
  scrollBehavior() {
    return {
      top: 0
    }
  }
})

export default router

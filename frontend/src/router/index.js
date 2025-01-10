import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DeleteView from '../views/DeleteView.vue'
import TeamView from '../views/TeamView.vue'
import SettingsView from '../views/SettingsView.vue'
import LogView from '../views/LogView.vue'
const router = createRouter({
  mode:'hash',
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/delete',
      name: 'delete',
      component: DeleteView,
    },
    {
      path: '/team',
      name: 'team',
      component: TeamView,
    },
    {
      path: '/settings',
      name: 'settings',
      component: SettingsView,
    },
    {
      path: '/log',
      name: 'log',
      component: LogView,
    },
  ],
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import RecordList from './views/RecordList.vue'

const routes = [
  {
    path: '/',
    name: 'records',
    component: RecordList
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '@/views/Index.vue'
import Home from '@/views/Home.vue'
import People from '@/views/People.vue'
import Detail from '@/views/Detail.vue'
import Profile from '@/views/Profile.vue'
import SearchResult from '@/views/SearchResult.vue'
import ReleaseSchedule from '@/views/ReleaseSchedule'


Vue.use(VueRouter)

const routes = [
  {
    path: '',
    name: 'Index',
    component: Index
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/people',
    name: 'People',
    component: People
  },
  {
    path: '/detail/:movie_id',
    name: 'Detail',
    component: Detail
  },
  {
    path: '/:username/profile',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/search/:keyword',
    name: 'SearchResult',
    component: SearchResult,
    props: true,
  },
  {
    path: '/release',
    name: 'ReleaseSchedule',
    component: ReleaseSchedule,
  },

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

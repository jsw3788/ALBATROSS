import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import People from '@/views/People.vue'
import Detail from '@/views/Detail.vue'
import Profile from '@/views/Profile.vue'
import Review from '@/views/Review.vue'

Vue.use(VueRouter)

const routes = [
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
    path: '/detail',
    name: 'Detail',
    component: Detail
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/review',
    name: 'Review',
    component: Review
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

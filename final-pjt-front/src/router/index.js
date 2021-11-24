import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import People from '@/views/People.vue'
import Detail from '@/views/Detail.vue'
import Profile from '@/views/Profile.vue'
import SearchResult from '@/views/SearchResult.vue'
import PeopleDirectorDetail from '@/views/detail/PeopleDirectorDetail'
import PeopleActorDetail from '@/views/detail/PeopleActorDetail'


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
    path: '/detail/:movie_id',
    name: 'Detail',
    component: Detail
  },
  {
    path: '/people/director/:director_pk',
    name: 'PeopleDirectorDetail',
    component: PeopleDirectorDetail
  },
  {
    path: '/people/actor/:actor_pk',
    name: 'PeopleActorDetail',
    component: PeopleActorDetail
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
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

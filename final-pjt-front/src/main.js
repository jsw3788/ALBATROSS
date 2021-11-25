import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'


import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)


import StarRating from 'vue-star-rating'
Vue.component('star-rating', StarRating);


import Notifications from 'vue-notification'
Vue.use(Notifications)


import VueCarousel from 'vue-carousel';
Vue.use(VueCarousel);


import anime from 'animejs/lib/anime.es.js'
Vue.prototype.$anime = anime;


import VCalendar from 'v-calendar';

// Use v-calendar & v-date-picker components
Vue.use(VCalendar);

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

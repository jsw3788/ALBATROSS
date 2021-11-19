import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    actors: [],
    directors: []
  },
  mutations: {
    GET_ACTORLIST: function (state, res) {
      state.actors = res.data
      // console.log(state.actors)
    },

    GET_DIRECTORLIST: function (state, res) {
      state.directors = res.data
      // console.log(state.directors)
    },
  },
  actions: {
    getPeople: function ({ commit }) {

      // 감독 리스트 가져오기
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/people/directors/',
      }).then(res =>{
        commit('GET_DIRECTORLIST',res)

      }).catch(err => {console.log(err)})
      
      // 배우 리스트 가져오기
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/people/actors/',
      }).then(res =>{
        commit('GET_ACTORLIST',res)

      }).catch(err => {console.log(err)})
      
    }
  },
  modules: {
  }
})

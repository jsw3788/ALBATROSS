import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from '../router'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    popularMovies: null,
    recommendMovies: null,
    releasedMovies: null,
    scoreMovies: null,
    actors: [],
    directors: [],
    jwtToken: localStorage.getItem("jwt"),
    username: localStorage.getItem("username"),
  },
  mutations: {
    SET_TOKEN: function (state, token) {
      localStorage.setItem("jwt", token);
      state.jwtToken = token
    },
    EXP_TOKEN: function (state) {
      localStorage.removeItem("jwt")
      state.jwtToken = null
    },
    GET_POPULAR_MOVIE_LIST: function (state, popularMovieList) {
      state.popularMovies = popularMovieList
    },
    GET_RECOMMEND_MOVIE_LIST: function (state, recommendMovieList) {
      state.recommendMovies = recommendMovieList
    },
    GET_RELEEASED_MOVIE_LIST: function (state, releasedMovieList) {
      state.releasedMovies = releasedMovieList
    },
    GET_SCORE_MOVIE_LIST: function (state, scoreMovieList) {
      state.scoreMovies = scoreMovieList
    },
    GET_ACTORLIST: function (state, res) {
      state.actors = res.data
      // console.log(state.actors)
    },

    GET_DIRECTORLIST: function (state, res) {
      state.directors = res.data
      // console.log(state.directors)
    },
    SET_USERNAME: function(state, username) {
      localStorage.setItem("username", username);
      state.username = username
    },
    EXP_USERNAME: function(state) {
      localStorage.removeItem("username")
      state.username = null
    }
  },
  actions: {
    login: function ({ commit }, credentials) {
      console.log(credentials)
      axios({
        method: "post",
        url: `${process.env.VUE_APP_SERVER_URL}/api/v2/api-token-auth/`,
        data: credentials,
      })
        .then(res => {
          commit("SET_TOKEN", res.data.token)
          router.go()
        })
        .catch(err => {
          console.log(err)
          // swal("아이디와 비밀번호를 확인하쇼", {
          //   dangerMode: true,
          // })
        })
    },
    logout: function ({ commit }) {
      commit("EXP_TOKEN")
      commit("EXP_USERNAME")
    },
    setUsername: function ({ commit }, username) {
      commit('SET_USERNAME', username)
    },
    
    getPopularMovies: function ({ commit }, popularMovieList) {
      commit('GET_POPULAR_MOVIE_LIST', popularMovieList)
    },
    getRecommendMovies: function ({ commit }, recommendMovieList) {
      commit('GET_RECOMMEND_MOVIE_LIST', recommendMovieList)
    },
    getReleasedMovies: function ({ commit }, releasedMovieList) {
      commit('GET_RELEEASED_MOVIE_LIST', releasedMovieList)
    },
    getScoreMovies: function ({ commit }, scoreMovieList) {
      commit('GET_SCORE_MOVIE_LIST', scoreMovieList)
    },
    getPeople: function ({ commit }) {

      // 감독 리스트 가져오기
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/people/directors/',
      }).then(res => {
        commit('GET_DIRECTORLIST', res)

      }).catch(err => { console.log(err) })

      // 배우 리스트 가져오기
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/people/actors/',
      }).then(res => {
        commit('GET_ACTORLIST', res)

      }).catch(err => { console.log(err) })
    },
  },
  getters: {
    isLogin: function (state) {
      return state.jwtToken ? true : false
    },
    config: function (state) {
      return {
        Authorization: `JWT ${state.jwtToken}`
      }
    }
  },
  modules: {
  },
})

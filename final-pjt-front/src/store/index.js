import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    popularMovies: null,
    recommendMovies: null,
    releasedMovies: null,
    scoreMovies: null,
    actors: [],
    directors: [],
    username: null,
  },
  mutations: {
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
      state.username = username
    }
  },
  actions: {
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
  modules: {
  },
})

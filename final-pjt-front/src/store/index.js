import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    popularMovies: null,
    recommendMovies: null,
    releasedMovies: null,
    scoreMovies: null,
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
  },
  actions: {
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
  },
  modules: {
  }

})

<template>
  <input type="text" @input="searchPattern" v-model.trim="pattern">
  
</template>

<script>
import Fuse from 'fuse.js'
import { mapState } from "vuex"
import axios from 'axios'



export default {
  name: 'SearchBar',
  data: function () {
    return {
      pattern: null,
      result: [],
    };
  },
  methods: {
    searchPattern: function() {
      const options = {
      // isCaseSensitive: false,
      // includeScore: false,
      // shouldSort: true,
      // includeMatches: false,
      // findAllMatches: false,
      // minMatchCharLength: 1,
      // location: 0,
      // threshold: 0.6,
      // distance: 100,
      // useExtendedSearch: false,
      // ignoreLocation: false,
      // ignoreFieldNorm: false,
      keys: ["title",
        "genres.name",
        "actors.name",
        "directors.name"
      // [
      //   "genres",
      //   "actors",
      //   "directors"
        
      // ]
      ]};

      const fuse = new Fuse(this.allmovies, options);

      // Change the pattern
      // const pattern = ""

      this.result =  fuse.search(this.pattern)
      console.log(this.result)
    },
  },
  computed: {
    ...mapState(["allmovies"]),
  },
  created: function () {
    axios({
      method: "get",
      url: `${process.env.VUE_APP_SERVER_URL}/api/v1/movies/all/`,
      headers: this.$store.getters.config,
    }).then(res => {
      this.$store.dispatch('getAllMovies',res.data)
    })
  },
  
}
</script>

<style>

</style>
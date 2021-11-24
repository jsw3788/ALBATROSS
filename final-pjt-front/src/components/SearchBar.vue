<template>
  <input
    type="text"
    @input="searchPattern"
    @key.up="searchPattern"
    v-model.trim="pattern"
  />
</template>

<script>
import Fuse from "fuse.js";
import { mapState } from "vuex";

export default {
  name: "SearchBar",
  data: function () {
    return {
      pattern: null,
      result: [],
    };
  },
  methods: {
    searchPattern() {
      if (this.pattern.length) {
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
          keys: [
            "title",
            "genres.name",
            "actors.name",
            "directors.name",
            // [
            //   "genres",
            //   "actors",
            //   "directors"

            // ]
          ],
        };

        const fuse = new Fuse(this.allmovies, options);

        // Change the pattern
        // const pattern = ""

        this.result = fuse.search(this.pattern);
        console.log(this.result);
        this.$router.push({
          name: "SearchResult",
          params: { keyword: this.pattern, result: this.result },
        });
      } else {
        console.log("메롱");
        this.$router.push({
          name: "Home",
        });
      }
    },
  },
  computed: {
    ...mapState(["allmovies"]),
  },
};
</script>

<style>
</style>
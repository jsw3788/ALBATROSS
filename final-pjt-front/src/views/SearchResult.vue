<template>
  <b-container class="bv-example-row">
    <h4>검색결과</h4>
    <b-row>
      <b-col cols="2" v-for="ret in result" :key="ret.item.id">
        <img :src="ret.item.poster_path" alt="poster" style="width: 100%" />
        <p>{{ ret.item.title }}</p>
        <span v-for="(genre, index) in ret.item.genres" :key="genre + index">
          {{ genre.name }}
        </span>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: "SearchResult",
  props: {
    result: Array,
  },
};
</script>

<style>
</style>
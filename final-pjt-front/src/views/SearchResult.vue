<template>
  <b-container class="bv-example-row">
    <h4 class="mt-5">검색결과</h4>
    <b-row>
      <b-col
        xl="3"
        md="4"
        cols="6"
        class="mt-2"
        v-for="ret in result"
        :key="ret.item.id"
      >
        <div @click="goDetailInfo(ret.item)" class="poster p-2">
          <img
            :src="ret.item.poster_path"
            alt="poster"
            style="width: 100%"
            class="poster-img"
          />
          <p class="poster-text">{{ ret.item.title }}</p>
        </div>
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
  methods: {
    goDetailInfo: function (movie) {
      this.$router.push({
        name: "Detail",
        params: {
          movie_id: movie.id,
        },
      });
    },
  },
};
</script>

<style scoped>
.poster-img {
  vertical-align: top;
}
.poster {
  display: inline-block;
  position: relative;
}
.poster:hover:after,
.poster:hover > .poster-text {
  display: block;
}
.poster:after,
.poster-text {
  display: none;
}

.poster:after {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 10;
}
.poster {
  overflow: hidden;
}
.poster .poster-img {
  height: 340px;
}
.poster:hover .poster-img {
  transform: scale(1.2);
  transition: 1s;
}
.poster-text {
  position: absolute;
  margin-left: auto;
  margin-right: auto;
  top: 5%;
  color: #fff;
  z-index: 20;
  font-weight: 600;
  font-size: 20px;
}
</style>

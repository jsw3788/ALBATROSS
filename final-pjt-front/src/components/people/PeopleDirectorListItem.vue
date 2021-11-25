<template>
  <b-col lg="2" md="3" sm="4" cols="6" class="mt-2">
    <div>
      <img :src="director.profile_path" style="width: 100%" />
    </div>
    <div no-body class="mb-1">
      <div>
        <b-row>
          <b-col @click="getDirector" v-b-toggle="'accordion-2' + director.id"
            >{{ director.name }} <b-icon-film></b-icon-film
          ></b-col>
        </b-row>
      </div>
    </div>
    <b-collapse
      :id="'accordion-2' + director.id"
      accordion="my-accordion"
      role="tabpanel"
    >
      <div
        v-for="movie in movies"
        :key="movie.title"
        class="d-flex flex-wrap justify-content-center"
      >
        <p>{{ movie.title }}</p>
        <div>
          <img :src="movie.poster_path" alt="" style="width: 100%" />
        </div>
      </div>
    </b-collapse>
  </b-col>
</template>

<script>
import axios from "axios";

export default {
  name: "PeopleDirectorListItem",
  props: {
    director: Object,
  },
  data: function () {
    return {
      movies: null,
    };
  },
  methods: {
    getDirector: function () {
      axios({
        method: "get",
        url: `http://127.0.0.1:8000/api/v1/people/directors/${this.director.id}`,
      })
        .then((res) => {
          this.movies = res.data.movies;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style>
</style>
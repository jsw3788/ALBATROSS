<template>
  <b-col lg="2" md="3" sm="4" cols="6" class="mt-2">
    <div>
      <img :src="actor.profile_path" style="width: 100%" />
    </div>
    <div no-body class="mb-1">
      <div>
        <b-row>
          <b-col @click="getActorDetail" v-b-toggle="'accordion-1' + actor.id"
            >{{ actor.name }} <b-icon-film></b-icon-film
          ></b-col>
        </b-row>
      </div>
    </div>
    <b-collapse
      :id="'accordion-1' + actor.id"
      accordion="my-accordion"
      role="tabpanel"
    >
      <div
        v-for="movie in movies"
        :key="movie.title"
        class="d-flex flex-wrap justify-content-center mb-2"
      >
        <div>{{ movie.title }}</div>
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
  name: "PeopleActorListItem",
  props: {
    actor: Object,
  },
  data: function () {
    return {
      movies: null,
    };
  },
  methods: {
    getActorDetail: function () {
      axios({
        method: "get",
        url: `http://127.0.0.1:8000/api/v1/people/actors/${this.actor.id}`,
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
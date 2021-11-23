<template>
  <b-col cols="2">
    <div @click="goToDirectorDetail">
      <img :src="director.profile_path" style="width: 100%" />
      <p>{{ director.name }}</p>
      <p>{{ director.popularity }}</p>
    </div>
  </b-col>
</template>

<script>
export default {
  name: "PeopleDirectorListItem",
  props: {
    director: Object,
  },
  methods: {
    goToDirectorDetail: function () {
      this.$router.push({
        name: "PeopleDirectorDetail",
        params: { director_pk: this.director.id },
      });
    },
  },
};
</script>

<style>
</style>
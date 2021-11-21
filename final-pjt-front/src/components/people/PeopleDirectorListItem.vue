<template>
  <div @click="goToDirectorDetail">
    <img :src="director.profile_path" style="width: 10%" />
    <p>{{ director.name }}</p>
    <p>{{ director.popularity }}</p>
  </div>
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
<template>
  <div @click="goToDirectorDetail">
    <li>
      <img :src="director.profile_path">
      {{ director.name }}
      {{ director.popularity }}

    </li>
  </div>
</template>

<script>
export default {
  name: 'PeopleDirectorListItem',
  props: {
    director: Object,
  },
  methods: {
    goToDirectorDetail: function () {
      this.$router.push({ name: 'PeopleDirectorDetail' , params: { director_pk: this.director.id } })
    }
  }
}
</script>

<style>

</style>
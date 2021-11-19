<template>
  <div>
    <people-actor-list></people-actor-list>
    <people-director-list></people-director-list>
  </div>
</template>

<script>
import PeopleActorList from '@/components/PeopleActorList'
import PeopleDirectorList from '@/components/PeopleDirectorList'

export default {
  name: "People",
  components: {
    PeopleActorList,
    PeopleDirectorList
  },
  created: function () {
    this.$store.dispatch('getPeople')
  }
};
</script>

<style>
</style>
<template>
  <div>
    <h1>인기 배우</h1>
    <people-actor-list></people-actor-list>

    <h1>인기 감독</h1>
    <people-director-list></people-director-list>
  </div>
</template>

<script>
import PeopleActorList from "@/components/people/PeopleActorList";
import PeopleDirectorList from "@/components/people/PeopleDirectorList";

export default {
  name: "People",
  components: {
    PeopleActorList,
    PeopleDirectorList,
  },
  created: function () {
    this.$store.dispatch("getPeople");
  },
};
</script>

<style>
</style>
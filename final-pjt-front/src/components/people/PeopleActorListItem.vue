<template>
  <b-col cols="2">
    <div @click="goToActorDetail">
      <img :src="actor.profile_path" style="width: 100%" />
      <p>{{ actor.name }}</p>
      <p>{{ actor.popularity }}</p>
    </div>
  </b-col>
</template>

<script>
export default {
  name: "PeopleActorListItem",
  props: {
    actor: Object,
  },
  methods: {
    goToActorDetail: function () {
      this.$router.push({
        name: "PeopleActorDetail",
        params: { actor_pk: this.actor.id },
      });
    },
  },
};
</script>

<style>
</style>
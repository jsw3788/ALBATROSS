<template>
  <div @click="goToActorDetail">
    <img :src="actor.profile_path" style="width: 10%" />
    <p>{{ actor.name }}</p>
    <p>{{ actor.popularity }}</p>
  </div>
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
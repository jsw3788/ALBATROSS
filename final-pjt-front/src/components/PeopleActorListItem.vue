<template>
  <div @click="goToActorDetail">
    <li>
      <img :src="actor.profile_path">
      {{ actor.name }}
      {{ actor.popularity }}

    </li>
  </div>
</template>

<script>
export default {
  name: 'PeopleActorListItem',
  props: {
    actor: Object,
  },
  methods: {
    goToActorDetail: function () {
      this.$router.push({ name: 'PeopleActorDetail' , params: { actor_pk: this.actor.id } })
    }
  }
}
</script>

<style>

</style>
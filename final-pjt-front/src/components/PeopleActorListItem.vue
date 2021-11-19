<template>
  <div>
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

  }
}
</script>

<style>

</style>
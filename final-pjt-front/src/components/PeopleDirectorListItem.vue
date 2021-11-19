<template>
  <div>
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

  }
}
</script>

<style>

</style>
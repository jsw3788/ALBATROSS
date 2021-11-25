<template>
  <div>
    <h1 class="mt-5">HOT ACTORS</h1>
    <div>
      <people-actor-list></people-actor-list>
    </div>
    <hr />
    <h1 class="mt-5">HOT DIRECTORS</h1>
    <div>
      <people-director-list></people-director-list>
    </div>
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
};
</script>

<style>
</style>
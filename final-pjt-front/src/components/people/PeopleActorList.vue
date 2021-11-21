<template>
  <div>
    <ul>
      <people-actor-list-item
        v-for="actor in actors"
        :key="actor.actor_id"
        :actor="actor"
      >
      </people-actor-list-item>
    </ul>
  </div>
</template>

<script>
import { mapState } from "vuex";
import PeopleActorListItem from "@/components/people/PeopleActorListItem";

export default {
  name: "PeopleActorList",
  components: {
    PeopleActorListItem,
  },
  computed: {
    ...mapState(["actors"]),
  },
};
</script>

<style>
</style>
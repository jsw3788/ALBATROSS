<template>
  <div>
    <ul>
      <people-director-list-item
        v-for="director in directors"
        :key="director.director_id"
        :director="director"
      >
      </people-director-list-item>
    </ul>
  </div>
</template>

<script>
import { mapState } from "vuex";
import PeopleDirectorListItem from "@/components/people/PeopleDirectorListItem";

export default {
  name: "PeopleDirectorList",
  components: {
    PeopleDirectorListItem,
  },
  computed: {
    ...mapState(["directors"]),
  },
};
</script>

<style>
</style>
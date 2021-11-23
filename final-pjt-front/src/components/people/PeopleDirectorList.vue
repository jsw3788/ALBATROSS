<template>
  <b-container class="bv-example-row">
    <b-row>
      <people-director-list-item
        v-for="director in directors"
        :key="director.director_id"
        :director="director"
      >
      </people-director-list-item>
    </b-row>
  </b-container>
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
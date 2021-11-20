<template>
  <div>
    <span>
      <img :src="image" alt="no profile">
      <p>{{username}}</p>
    </span>
    <div>
      films | {{films}}
      follower | {{follower}}
      following | {{following}}
    </div>
    <div v-if="!isMySelf">
      <button v-if="isfollowing" @click="follow">
        Unfollow
      </button>
      <button v-else @click="follow">
        Follow
      </button>
    </div>
    <profile-movie></profile-movie>
    <profile-review></profile-review>
  </div>
</template>

<script>
import axios from 'axios'
import ProfileMovie from '@/components/ProfileMovie.vue'
import ProfileReview from '@/components/ProfileReview.vue'
import { mapGetters } from 'vuex'

export default {
  name: 'Profile',
  components: {
    ProfileMovie,
    ProfileReview,
  },
  data: function() {
    return {
      username: null,
      follower: null,
      following: null,
      isfollowing: null,
      image: null,
      films: null,
    }
  },
  methods:{
    follow: function() {
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/api/v2/${this.username}/follow/`,
        headers: this.Config
      }).then(res =>{
        this.isfollowing = res.data.following
        this.follower = res.data.followingCnt
        this.following = res.data.followerCnt
      })
    }
  },
  created: function () {
    axios({
        method: 'get',
        url: `http://127.0.0.1:8000/api/v2/${this.$route.params.username}/profile/`,
        headers: this.Config
        
      }).then(res => {
        
        this.username = res.data.username
        this.isfollowing = res.data.following
        this.following = res.data.followingCnt
        this.follower = res.data.followerCnt
        this.image = res.data.profile_image
        this.films = res.data.movieCnt


      }).catch(err => { console.log(err) })
  },
  computed: {
    isMySelf: function () {
      if (this.username != localStorage.getItem("username")){
        return false
      }
      else{
        return true
      }
    },
    ...mapGetters([
      'Config'
    ])
  }

}
</script>

<style>

</style>
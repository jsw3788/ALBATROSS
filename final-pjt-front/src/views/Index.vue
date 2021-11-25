<template>
  <div>
    <h1 class="ml9" style="height: 100vh">
      <div style="margin: auto">
        <span class="text-wrapper">
          <span class="letters">ALBATROSS</span>
        </span>
      </div>
    </h1>
  </div>
</template>

<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/2.0.2/anime.min.js"></script>
<script src="anime.min.js"></script>
<script>
import anime from "animejs/lib/anime.es.js";

export default {
  name: "Index",
  data: function () {
    return {
      isIndex: true,
    };
  },
  mounted: function () {
    setTimeout(() => {
      // anime
      // Wrap every letter in a span
      let textWrapper = document.querySelector(".ml9 .letters");
      textWrapper.innerHTML = textWrapper.textContent.replace(
        /\S/g,
        "<span class='letter'>$&</span>"
      );

      anime
        .timeline({ loop: true })
        .add({
          targets: ".ml9 .letter",
          scale: [0, 1],
          duration: 1500,
          elasticity: 600,
          delay: (el, i) => 45 * (i + 1),
        })
        .add({
          targets: ".ml9",
          opacity: 0,
          duration: 1000,
          easing: "easeOutExpo",
          delay: 1000,
        });

      // setTimeout(() => {
      //   this.$router.push({ name: "Home" });
      // }, 3000);
    }, 1000);
  },
};
</script>

<style>
.ml9 {
  position: relative;
  font-weight: 200;
  font-size: 4em;
}
.ml9 .text-wrapper {
  position: relative;
  display: inline-block;
  padding-top: 0.2em;
  padding-right: 0.05em;
  padding-bottom: 0.1em;
  overflow: hidden;
}
.ml9 .letter {
  position: relative;
  transform-origin: 50% 100%;
  display: inline-block;
  line-height: 1em;
}
</style>
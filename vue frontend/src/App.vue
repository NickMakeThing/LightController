<template>

  <!-- <img height='50' alt="Vue logo" src="./assets/logo.png"> -->
  <div id='main-container'>
    <ColorPicker />

  </div>
  <!-- <BrightnessSlider /> -->
</template>

<script>
import BrightnessSlider from './components/BrightnessSlider.vue'
import ColorPicker from './components/ColorPicker.vue'

export default {
  name: 'App',
  components: {
    // BrightnessSlider,
    ColorPicker
  }
}
</script>

<style>
#main-container{
  height:100vh;
  width:100vw;
  padding:8px;
  //background: red;
}
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
</style>

<template>

  <!-- <img height='50' alt="Vue logo" src="./assets/logo.png"> -->
  <div id='main-container'>
    <LightBulb :color='color'/>
    <ColorPicker @colorToParent='colorChange'/>
  </div>
  <!-- <BrightnessSlider /> -->
</template>

<script>
import BrightnessSlider from './components/BrightnessSlider.vue'
import ColorPicker from './components/ColorPicker.vue'
import LightBulb from './components/LightBulb.vue'

export default {
  name: 'App',
  components: {
    // BrightnessSlider,
    LightBulb,
    ColorPicker
  },
  data(){
    return{
      color:null,
      colorProp:null
    }
  },
  methods: {
    colorChange(color){
      this.color = color
    },
  }
}
</script>

<style>
#main-container{
  display:flex;
  flex-direction:column;
  gap:25px;
  margin-top:50px;
  align-items:center;
  height:100vh;
  width:100vw;
  padding:8px;
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

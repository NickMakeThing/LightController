<template>
  <div id='page-container'>
    <RainbowBackground />
    <div id='main-container'>
      <div id='picker-container'>
        <LightBulb :color='color'/>
        <ColorPicker @colorToParent='colorChange'/>
      </div>
      <div id='changes-container'>
        <AutoChange v-for="change in changeList" :key='change.id'
          :time='change.time' 
          :color='{r:change.red, g:change.green, b:change.blue}'
          :id='change.id'
          :getChanges='getChanges'
        />
        <AutoChangeForm :color='color' :getChanges='getChanges'/>
      </div>
    </div>
  </div>
</template>

<script>
  import AutoChange from './components/AutoChange.vue'
  import AutoChangeForm from './components/AutoChangeForm.vue'
  import ColorPicker from './components/ColorPicker.vue'
  import LightBulb from './components/LightBulb.vue'
  import RainbowBackground from './components/RainbowBackground.vue'
   
  export default {
    name: 'App',
    components: {
      LightBulb,
      ColorPicker,
      AutoChange,
      AutoChangeForm, 
      RainbowBackground
    },
    data(){
      return{
        color:null,
        changeList:[]
      }
    },
    beforeMount(){
      this.getChanges()
    },
    methods: {
      colorChange(color){
        this.color = color
      },
      async getChanges(){
        this.changeList = await fetch('http://127.0.0.1:8000/get')
        .then(data => data.json())
      }
    },
  }
</script>

<style>
  #page-container{
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    width:100%;
  }
  #main-container{
    display:flex;
    justify-content:center;
    gap:25px;
    padding:30px;
    border: solid 3px rgba(199,199,199);

    border-radius:5%;
    background:rgba(255,255,255,1);
    box-shadow: 0px 0px 13px black;
  }
  #picker-container{
    display:flex;
    flex-direction:column;
    gap:25px;
  }
  #changes-container{
    display:flex;
    flex-direction:column;
    align-items: center;
    font-family: Arial, sans-serif;
    width: 230px;
    height: 550px; 
    overflow: auto;
    scrollbar-width: thin;
  }
  </style>

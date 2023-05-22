<template>
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
</template>

<script>
  import AutoChange from './components/AutoChange.vue'
  import AutoChangeForm from './components/AutoChangeForm.vue'
  import ColorPicker from './components/ColorPicker.vue'
  import LightBulb from './components/LightBulb.vue'
   
  export default {
    name: 'App',
    components: {
      LightBulb,
      ColorPicker,
      AutoChange,
      AutoChangeForm, 
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
  #main-container{
    display:flex;
    gap:25px;
    margin-top:50px;
    justify-content:center;
    height:100vh;
    width:100vw;
    padding:8px;
  }
  #picker-container{
    display:flex;
    flex-direction:column;
    gap:25px;
  }
  #changes-container{
    font-family: Arial, sans-serif;
    border: solid 1px black;
    width: 230px;
    height: 550px; 
    border-radius: 5px;
  }
  </style>

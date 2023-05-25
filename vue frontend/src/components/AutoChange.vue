<template>
    <div class='change'>
        <button @click='deleteChange'>delete</button> <!-- change to bin icon -->
        <div class='change-time'>{{computedTime}}</div>
        <div class='change-colour-container'>
          <div class='change-colour' :style='`background:rgb(${computedColor});`'>
          </div>
          <div>
            {{computedColor}}
          </div>
        </div>
    </div>
</template>

<script>
  export default {
    name: 'AutoChange',
    props:['time','color','id','getChanges'],
    computed:{
      computedTime(){
        return this.time.slice(0,-3)
      },
      computedColor(){
        return `${this.color.r},${this.color.g},${this.color.b}`
      }
    },
    methods: {
      async deleteChange(){
        await fetch('http://127.0.0.1:8000/delete/' + this.id, {method: 'DELETE'})
        this.getChanges() //todo: just return list data in response to delete instead
      },
    },
  }
</script>

<style scoped>
  .change{
    height: 50px;
    max-width:90%;
    padding:5px;
    border-radius: 5px;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    align-items: center;
    justify-items: center;
    box-shadow: 0px 1px 5px black;
    margin-top: 5px;
    margin-bottom: 5px;
  }
  .change-time{
    font-size:180%;
  }
  .change-colour-container{
    display:flex;
    flex-direction:column;
    align-items:center;
    font-size:80%;
  }
  .change-colour{
    height:30px;
    width:30px;
    border-radius:5px;
  }
</style>

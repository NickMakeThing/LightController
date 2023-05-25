<template>
    <div id='change-form'>
        <button @click='postColorChange'>create</button>
        <input id='change-form-time' type="time" v-model='time'/>
    </div>
</template>

<script>
  export default {
    name: 'AutoChangeForm',
    props: ['color','getChanges'],
    data() {
      return {
        time:'13:00'
      }

    }, 
    methods: {
      async postColorChange(){
        let colorChange = {
          time: this.time,
          red: this.color.r,
          green: this.color.g,
          blue: this.color.b 
        }
        let response = await fetch('http://127.0.0.1:8000/create', {
              method : 'POST',
              headers: { "Content-Type": "application/json" },
              body : JSON.stringify(colorChange)
            }
        )
        this.getChanges() //todo: just return list data in response to delete instead
      }
    }
  }
</script>

<style scoped>
  #change-form{
    height: 50px;
    width:90%;
    padding:5px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap:15px;
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
  #change-form-time{
    border-radius:3px;
  }
</style>

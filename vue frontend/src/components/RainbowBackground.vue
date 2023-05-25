<template>
    <canvas height="32" width="32" ref=background />
</template>

<script>
    export default {
        name: 'AutoChangeForm',
        mounted(){
            var backgroundRef = this.$refs.background;
            var context = backgroundRef.getContext('2d');
            var t = 0;
            this.run(t,context);
        },
        methods:{
            //https://codepen.io/tmrDevelops/pen/vOPZBv
            R(x, y, t){
                return( Math.floor(192 + 128*Math.cos( (x*x-y*y)/300 + t )) );
            },
            G(x, y, t){
                return( Math.floor(192 + 128*Math.sin( (x*x*Math.cos(t/4)+y*y*Math.sin(t/3))/300 ) ) );
            },
            B(x, y, t){
                return( Math.floor(192 + 128*Math.sin( 5*Math.sin(t/9) + ((x-100)*(x-100)+(y-100)*(y-100))/1100) ));
            },
            col(x, y, r, g, b, context) {
                context.fillStyle = "rgb(" + r + "," + g + "," + b + ")";
                context.fillRect(x, y, 1,1);
            },
            run(t,context){
                for(let x=0;x<=35;x++) {
                    for(let y=0;y<=35;y++) {
                    this.col(x, y, this.R(x,y,t), this.G(x,y,t), this.B(x,y,t),context);
                    }
                }
                t = t + 0.03; //should  make it slower
                let callback = () => {this.run(t,context)}
                window.requestAnimationFrame(callback);
            }
        }
    }
</script>

<style scoped>
    canvas{
        position:absolute;
        top:0;
        width:100%;
        height:100%;
        z-index:-1;
    }
</style>
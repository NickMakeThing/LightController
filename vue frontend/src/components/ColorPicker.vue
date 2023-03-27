<template>
    <div id="color-picker-container">
        <div id="box-slider-container">
            <div 
                id='color-picker-box' 
                :style='boxGradient' @mousedown='boxMouseDown' 
                @mouseenter='boxMouseEnter' 
                @mouseleave='boxMouseLeave' 
                ref=colorPickerBox>
                <svg height="10" width="10" id="selectorCircle" :style="selectedPixelLocation" ref='selector'>
                    <circle cx="5" cy="5" r="4" stroke="white" stroke-width="2px" fill="none" />
                </svg>
            </div>
            <input v-model='hue' @mousedown='sliderMouseDown' id='hue-slider' type='range' max=360 />
            <div id='picked-color-numbers' @change='rgbNumbersChanged'> 
                <span>R<input class='rgb-input' type='number' v-model='pickedColor.r'></span>
                <span>G<input class='rgb-input' type='number' v-model='pickedColor.g'></span>
                <span>B<input class='rgb-input' type='number' v-model='pickedColor.b'></span>
            </div>
        </div>
        <div id='color-preview' :style='"background:rgb("+pickedColor.r+","+pickedColor.g+","+pickedColor.b+");"'></div>
    </div>
</template>

<script>
    import colorsys from 'colorsys'

    export default {
        name: 'ColorPicker',
        emits:['colorToParent'],
        data(){
            return {
                hue:120,
                brightness:0,
                mouseInBox:false,
                mouseDownBox:false,
                boxDimensions:null,
                pixelSelectedX:0,
                pixelSelectedY:-5,
                pickedColor:{r:0,g:0,b:0},

                mouseDownSlider:false,
            }
        },
        mounted(){
            document.addEventListener("mousemove", this.pickColor)
            document.addEventListener("mouseup", this.pageMouseUp)
            this.boxDimensions = this.$refs.colorPickerBox.getBoundingClientRect()
            this.pixelSelectedX = this.boxDimensions.width - 5 // or just -5
            this.pickedColor = this.rgbAtCircle()
        },
        beforeUpdate(){
            //dimensions reassignment prevents the circle from appearing in wrong place after scrolling
            this.boxDimensions = this.$refs.colorPickerBox.getBoundingClientRect()
                // change this^ to happen on scroll events
            this.$emit('colorToParent', this.pickedColor)
        },
        computed:{
            boxGradient(){
                return `
                    background:linear-gradient(
                            hsla(${this.hue},100%,0%,0),
                            hsla(${this.hue},100%,0%,1)
                        ),
                    linear-gradient(
                        90deg,hsl(${this.hue},100%,100%),
                        hsl(${this.hue},100%,50%)
                    );
                `
            },
            selectedPixelLocation(){
                return 'top:'+this.pixelSelectedY+'px; left:'+this.pixelSelectedX+'px;'
            }
        },
        watch: {
            hue(){
                this.pickColorOnSliderMove()
            }
        },
        methods:{
            pageMouseUp(){
                if(this.mouseDownBox || this.mouseDownSlider){
                    this.mouseDownBox = false
                    this.mouseDownSlider = false
                    this.sendColor()
                }
            },
            boxMouseDown(){
                this.mouseDownBox = true
                this.pickColor()
            },
            boxMouseEnter(){
                this.mouseInBox = true
            },
            boxMouseLeave(){
                this.mouseInBox = false
            },
            pickColor(){
                if(this.mouseDownBox){
                    let mouse = { //x,y coords of inside the box
                        x: window.event.clientX - this.boxDimensions.x,
                        y: window.event.clientY - this.boxDimensions.y
                    }
                    this.pixelSelectedX = mouse.x - 5
                    this.pixelSelectedY = mouse.y - 5
                    if(this.mouseInBox){
                        this.pickedColor = this.rgbAtMouse(mouse)
                    } else {
                        this.moveCircleToBoxEdge()
                        this.pickedColor = this.rgbAtCircle()
                    }
                } 
            },
            rgbAtMouse(mouse){
                let saturation = mouse.x / this.boxDimensions.width * 100
                let value = 100 - mouse.y / this.boxDimensions.height * 100
                let rgb = colorsys.hsvToRgb({h:this.hue,s:saturation,v:value})
                this.brightness = value
                return rgb
            },
            rgbAtCircle(){
                //X is 4.5 because strange bug where 4 makes picked color go to 0,0,0 when mouse outside on left, 5 causes same bug bug on right
                //  for some reason 4.5 fixes both sides.
                let colorX = this.pixelSelectedX + 5
                let colorY = this.pixelSelectedY + 5
                let saturation = colorX / this.boxDimensions.width * 100
                let value = 100 - colorY / this.boxDimensions.height * 100
                let rgb = colorsys.hsvToRgb({h:this.hue,s:saturation,v:value})
                this.brightness = value
                return rgb
            },
            moveCircleToBoxEdge(){
                if (window.event.clientX > this.boxDimensions.right) {
                    this.pixelSelectedX = this.boxDimensions.width - 5
                } else if (window.event.clientX < this.boxDimensions.left){
                    this.pixelSelectedX = 0 - 5
                }

                if (window.event.clientY > this.boxDimensions.bottom) {
                    this.pixelSelectedY = this.boxDimensions.height - 5
                } else if (window.event.clientY < this.boxDimensions.top){
                    this.pixelSelectedY = 0 - 5 
                }
            },
            sliderMouseDown(){
                this.mouseDownSlider=true
            },
            pickColorOnSliderMove(event){
                if(this.mouseDownSlider){
                    this.pickedColor = this.rgbAtCircle()
                }
            },
            rgbNumbersChanged(){
                let hsv = colorsys.rgbToHsv(this.pickedColor)                
                this.pixelSelectedX = hsv.s / 100 * this.boxDimensions.width - 5
                this.pixelSelectedY = this.boxDimensions.height - hsv.v * this.boxDimensions.height/100 - 5
                this.hue = hsv.h
                this.brightness = hsv.v
                this.sendColor()
            },
            async sendColor(){
                var brightness = this.brightness 
                var color = [this.pickedColor.r,this.pickedColor.g,this.pickedColor.b].map(value => {
                    if(value === ''){
                        return 0
                    } else {
                        return value
                    }
                })
                let response = await fetch('http://127.0.0.1:8000',
                    {
                        method : 'POST',
                        headers: { "Content-Type": "application/json" },
                        body : JSON.stringify({color,brightness}) //breaks when i use this.* here
                    }
                )
            }
        }

    }
</script>

<style scoped>
#color-picker-container{
    display:flex;
    gap:30px;
}
#color-preview{
    display:none;
    width:50px;
    height:50px;
    border-radius:10%;
}
#box-slider-container{
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:15px
}
#color-picker-box{
    position:relative;
    height:150px;
    width:300px;
    border-radius:5px;

}
#selectorCircle{
    position:absolute;
    pointer-events: none;
}
#picked-color-numbers{
    width: 300px;
    display:flex;
    justify-content:space-evenly;
    align-items:center;
}
.rgb-input{
    width:50px;
    margin:5px;
}
#hue-slider::-moz-range-thumb{
    background:transparent; 
    animation-delay:2s;
}
#hue-slider::-webkit-slider-thumb{
    background:transparent;
}
#hue-slider{
    -webkit-appearance: none;
    width:300px;
    border-radius:10px;
    height:10px;
    background:linear-gradient(
            90deg,
            hsl(0,100%,50%),
            hsl(10,100%,50%),
            hsl(20,100%,50%),
            hsl(30,100%,50%),
            hsl(40,100%,50%),
            hsl(50,100%,50%),
            hsl(60,100%,50%),
            hsl(70,100%,50%),
            hsl(80,100%,50%),
            hsl(90,100%,50%),
            hsl(100,100%,50%),
            hsl(110,100%,50%),
            hsl(120,100%,50%),
            hsl(130,100%,50%),
            hsl(140,100%,50%),
            hsl(150,100%,50%),
            hsl(160,100%,50%),
            hsl(170,100%,50%),
            hsl(180,100%,50%),
            hsl(190,100%,50%),
            hsl(200,100%,50%),
            hsl(210,100%,50%),
            hsl(220,100%,50%),
            hsl(230,100%,50%),
            hsl(240,100%,50%),
            hsl(250,100%,50%),
            hsl(260,100%,50%),
            hsl(270,100%,50%),
            hsl(280,100%,50%),
            hsl(290,100%,50%),
            hsl(300,100%,50%),
            hsl(310,100%,50%),
            hsl(320,100%,50%),
            hsl(330,100%,50%),
            hsl(340,100%,50%),
            hsl(350,100%,50%),
            hsl(360,100%,50%)
        );
}
</style>
<template>
    <div class="bg" :style="{height: winHeight, left: bgLeft}"></div>
</template>

<script>
    export default {
        name: "background",
        computed :{
            winHeight(){
                return (window.innerHeight - 50) + "px";
            },
            bgLeft(){
                return (window.innerWidth / 100 * 2.5) + "px";
            }
        }
    }
</script>

<style scoped>
.bg{
    width: 95%;
    background-color: #f2f2f2;
    z-index: -1;
    position: absolute;
    top: 50px;
    opacity: 0.5;
}
</style>
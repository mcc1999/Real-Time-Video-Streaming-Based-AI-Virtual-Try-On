<template>
    <div>
        <el-carousel class="carousel" :interval="4000"  height="500px">
            <el-carousel-item v-for="item in img_list" :key="item.url">
                <img :src="item.url" alt />
            </el-carousel-item>
        </el-carousel>
    </div>
</template>

<script>
    export default {
        name: "carousel",
        data() {
            return {
                img_list: [
                    {url: require("../assets/carousel00.png")},
                    {url: require("../assets/carousel01.png")},
                    {url: require("../assets/carousel02.png")},
                    {url: require("../assets/carousel03.png")},
                ]
            }
        }
    }
</script>

<style scoped>
.carousel{
    margin-top: 50px;
    margin-left: 75px;
    margin-right: 75px;
}
.el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
}
.el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
}
.el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
}
</style>
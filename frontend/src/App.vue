<template>
    <div id="app">
        <topBar></topBar>
        <carousel v-if="index"></carousel>
        <background></background>
        <router-view></router-view>
    </div>
</template>

<script>
import topBar from "./components/topBar";
import carousel from "./components/carousel";
import background from "./components/background";
export default {
    name: 'App',
    computed: {
        index() {
            return this.$route.path === '/'
        }
    },
    components: {
        topBar,
        carousel,
        background
    }
}
</script>

<style>
#app {
    font-family: "Comic Sans MS", serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
}
</style>

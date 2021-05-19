<template>
    <div class="navbar">
        <img src="../assets/icon.jpg" alt="" @click="toIndex">
        <span class="site_tile" @click="toIndex">直播AI虚拟试衣</span>
        <span class="login" @click="toLogin" v-if="unLoginIn">登陆</span>
        <span v-if="unLoginIn">/</span>
        <span class="signIn" @click="toSignIn" v-if="unLoginIn">注册</span>
        <router-link :to="{path: 'userCenter'}" v-if="username" class="aTag">{{ username }}</router-link>
        <span v-if="username">/</span>
        <span v-if="username" @click="toLogout" class="logout">注销</span>
    </div>
</template>

<script>
    export default {
        name: "topBar",
        data() {
            return {
                username: ''
            }
        },
        methods: {
            toIndex(){
                this.$router.push('/')
            },
            toLogin(){
                this.$router.push('/login')
            },
            toSignIn(){
                this.$router.push('/register')
            },
            toLogout(){
                this.axios.get("http://127.0.0.1:8000/users/logout")
                .then(res => {
                    if(res.data["msg_code"] === 100){
                        this.username = false
                        this.$router.push('/')
                    }else{
                        this.$message({"type": "warning", "message": "注销失败，请重试！"})
                    }
                })
                .catch( reason => {
                    this.$message({"type": "warning", "message": reason})
                })
            }
        },
        watch:{
            $route:{
                handler(){
                    this.axios.get('http://127.0.0.1:8000/users/getUser').then( res => {this.username = res.data.username})
                },
                immediate: true
            }
        },
        computed: {
            unLoginIn: function (){
                return !this.username
                // return (this.$route.path === '/register' || this.$route.path === '/login' || this.$route.path === '/') && this.username === ""
            },
            // username: function(){
            //     let uname = ''
            //     this.axios.get('http://127.0.0.1:8000/users/getUser').then( res => {uname = res.data.username})
            //     return uname
            // }
        },
    }
</script>

<style scoped>
.navbar{
    width: 100%;
    height: 50px;
    display: flex;
    align-items: center;
    background-color: #334466;
    font-family: "Comic Sans MS", serif;
}
img{
    width: 40px;
    height: 40px;
    margin-left: 50px;
    margin-right: 25px;
    border-radius: 5px;
}
.site_tile{
    font-size: 30px;
    color: #ffffff;
}
.login{
    margin-left: auto;
    margin-right: 10px;
    padding: 1px;
    border: #ffffff 2px solid;
    border-radius: 10%;
}
.signIn{
    margin-left: 10px;
    margin-right: 50px;
    padding: 1px;
    border: #ffffff 2px solid;
    border-radius: 10%;
}
.aTag{
    margin-left: auto;
    color: #ffffff;
    /*padding: 2px;*/
    /*border: 2px black solid;*/
    /*border-radius: 10%;*/
}
.logout{
    margin-right: 50px;
}
span{
    color: #ffffff;
}
</style>
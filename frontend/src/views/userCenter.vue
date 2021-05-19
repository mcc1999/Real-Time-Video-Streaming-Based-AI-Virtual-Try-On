<template>
    <div class="userCenter">
        <div class="content">
            <p>观看直播</p>
            <el-form :model="formInline00" class="demo-form-inline" label-position="left">
                <el-form-item label="房间号：" label-width="20%" class="el-input">
                    <el-input v-model="formInline00.roomNum" class="ipt"></el-input>
                </el-form-item>
                <el-form-item class="el-btn">
                    <el-button type="primary" class="btn" @click="onSearch">搜索</el-button>
                </el-form-item>
            </el-form>
        </div>
        <span></span>
        <div class="content">
            <p>成为主播</p>
            <el-form :model="formInline01" class="demo-form-inline" label-position="left">
                <el-form-item label="设置房间号：" label-width="20%" class="el-input">
                    <el-input v-model="formInline01.setRoomNum"></el-input>
                </el-form-item>
                <el-form-item class="el-btn">
                    <el-button type="primary" class="btn" @click="submitStartLive">开启直播</el-button>
                    <el-button type="primary" class="btn" @click="submitSignAnchor">注册主播</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
    export default {
        name: "userCenter",
        data() {
            return {
                formInline00: {
                    roomNum: '',
                },
                formInline01: {
                    setRoomNum: '',
                },
            }
        },
        methods: {
            onSearch() {
                let roomDta = new FormData();
                roomDta.append("roomNum", this.formInline00.roomNum);
                this.axios.post("http://127.0.0.1:8000/users/watchLive/", roomDta)
                    .then(res => {
                        if(res.data["msg_code"] === 100){
                            let roomInfo = res.data["meeting"]
                            this.$router.push({name: "watchLive", params: {meeting: roomInfo}})
                        }else {
                            this.$message({"type": "warning", "message": res.data["message"]})
                        }
                    })
                    .catch(reason => this.$message({"type": "warning", "message": reason}))
            },
            submitStartLive() {
                let liveData = new FormData();
                liveData.append('roomNum', this.formInline01.setRoomNum);
                this.axios.post("http://127.0.0.1:8000/users/startLive/", liveData)
                    .then(res => {
                        if(res.data["msg_code"] === 100){
                            let liveInfo = res.data["meeting"]
                            this.$store.commit("changeLiveInfo", liveInfo)
                            this.$router.push("/live")
                        }else {
                            this.$message({"type": "warning", "message": res.data["message"]})
                        }
                    })
                    .catch(reason => this.$message({"type": "warning", "message": reason}))
            },
            submitSignAnchor() {
                let roomData = new FormData();
                roomData.append('roomNum', this.formInline01.setRoomNum)
                this.axios.post("http://127.0.0.1:8000/users/signAnchor/", roomData)
                    .then(res => {
                        if(res.data["msg_code"] === 100){
                            this.$message({"type": "success", "message": res.data.message})
                        }else{
                            this.$message({"type": "warning", "message": res.data.message})
                        }
                    })
                    .catch(reason => this.$message({"type": "warning", "message": reason}))
            }
        }
    }
</script>

<style scoped>
.userCenter{
    display: flex;
    justify-content: center;
    margin-top: 75px;
}
.content{
    display: inline;
    padding: 20px;
    width: 40%;
    border: #797979 1px solid;
    border-radius: 5%;
    box-shadow: 10px 10px 10px #797979;
}
.content:first-of-type{
    margin-right: 2%;
}
.content:last-of-type{
    margin-left: 2%;
}
p{
    width: 80%;
    margin: 20px auto 100px auto;
    font-size: 50px;
    border-bottom: #797979 1px solid;
}
.el-input{
    margin-bottom: 50px;
}
.el-btn .btn{
    width: 30%;
    margin-bottom: 30px;
}
span{
    width: 1px;
    background-color: black;
}
button{
    background-color: #334466;
}
</style>
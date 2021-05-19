<template>
    <div class="watchLive">
        <div class="liveBox">
            <div class="live"></div>
        </div>
        <div class="screenShot">
            <span>点击右侧-截图-按钮，截取直播中的服饰</span>
            <el-button type="primary" class="shotBtn" @click="clothShot">截图</el-button>
            <el-button type="primary" class="shotBtn" @click="getClothImgUrl">查看服饰图片</el-button>
            <div class="shotCloth"><img :src="clothImgUrl" alt="" class="clothImg"></div>
            <span>若已截取到完整服饰，点击右侧-虚拟试衣-按钮进行试衣</span>
            <el-button type="primary" class="tryOnBtn" @click="toFittingRoom">虚拟试衣</el-button>
        </div>
    </div>
</template>

<script>
    import AgoraRTC from "agora-rtc-sdk-ng"
    let rtc = {
        // 用来放置本地客户端。
        client: null,
        // 用来放置本地音视频频轨道对象。
        localAudioTrack: null,
        localVideoTrack: null,
    };
    let options = {
        // 项目的 App ID。
        appId: '',
        // 传入目标频道名。
        channel: '',
        // 生成的 Token 值。
        token: '',
        // 设置频道内的用户角色，可设为 "audience" 或 "host"
        role: "audience",
        uid: null
    };
    export default {
        name: "watchLive",
        data() {
            return {
                clothImgUrl: '',
                clothObjectName: '',
                clothObjectKey: '',
                clothBytes: null
            }
        },
        methods: {
            watchLive(){
                let meetingInfo = this.$route.params.meeting;
                options.appId = meetingInfo["appID"];
                options.channel = meetingInfo["channel"];
                options.token = meetingInfo["token"];
                options.uid = meetingInfo["uid"];
                async function startBasicLive() {
                    // 创建客户端
                    rtc.client = AgoraRTC.createClient({ mode: "live", codec: "vp8" });
                    // 设置用户角色
                    rtc.client.setClientRole(options.role);
                    //加入目标频道
                    await rtc.client.join(options.appId, options.channel, options.token, options.uid);

                    rtc.client.on("user-published", async (user, mediaType) => {
                        // 开始订阅远端用户。
                        await rtc.client.subscribe(user, mediaType);
                        console.log("subscribe success");
                        // 表示本次订阅的是视频。
                        if (mediaType === "video") {
                            // 订阅完成后，从 `user` 中获取远端视频轨道对象。
                            const remoteVideoTrack = user.videoTrack;
                            // 动态插入一个 DIV 节点作为播放远端视频轨道的容器。
                            const playerContainer = document.createElement("div");
                            // 给这个 DIV 节点指定一个 ID，这里指定的是远端用户的 UID。
                            let liveBox = document.querySelector(".live")
                            playerContainer.id = user.uid.toString();
                            playerContainer.style.width = "300px";
                            playerContainer.style.height = "500px";
                            liveBox.append(playerContainer);
                            // 订阅完成，播放远端音视频。
                            // 传入 DIV 节点，让 SDK 在这个节点下创建相应的播放器播放远端视频。
                            // remoteVideoTrack.play(playerContainer);
                            let videoPlay = remoteVideoTrack.play(playerContainer);
                            if(videoPlay !== undefined){
                                videoPlay.then( () => {

                                })
                                    .catch(
                                        this.message({type:"warning","message":"直播播放错误，请重启直播间！"})
                                    )
                            }
                            // 也可以只传入该 DIV 节点的 ID。
                            // remoteVideoTrack.play(playerContainer.id);
                        }
                        // 表示本次订阅的是音频。
                        if (mediaType === "audio") {
                            // 订阅完成后，从 `user` 中获取远端音频轨道对象。
                            const remoteAudioTrack = user.audioTrack;
                            // 播放音频因为不会有画面，不需要提供 DOM 元素的信息。
                            let audioPlay = remoteAudioTrack.play();
                            if(audioPlay !== undefined){
                                audioPlay.then(() => {
                                    this.message({type:"warning","message":"直播播放错误，请重启直播间！"})
                                })
                                .catch()
                            }
                        }
                    });
                    rtc.client.on("user-unpublished", (user, mediaType) => {
                        if (mediaType === "video") {
                            // 获取刚刚动态创建的 DIV 节点。
                            const playerContainer = document.getElementById(user.uid.toString());
                            // 销毁这个节点。
                            playerContainer.remove();
                        }
                        rtc.client.leave();
                    });
                }
                startBasicLive();
            },
            clothShot(){
                let meetingData = new FormData();
                let meetingInfo = this.$route.params.meeting;
                meetingData.append("meeting", JSON.stringify(meetingInfo));
                this.axios.post("http://127.0.0.1:8000/api/clothShot/", meetingData)
                    .then(res => {
                        if(res.data["msg_code"] === 100){
                            this.$message({"type": "success", "message": res.data["message"]});
                            this.clothObjectName = res.data["cloth_object_name"];
                            console.log(this.clothObjectName);
                            this.getClothImgName(this.clothObjectName);
                        } else{
                            this.$message({"type": "warning", "message": res.data["message"]});
                        }
                    })
                    .catch(reason => this.$message({"type": "warning", "message": reason}));
            },
            getClothImgName(prefix){
                const OSS = require('ali-oss');

                const client = new OSS({
                    region: 'oss-cn-shanghai',
                    accessKeyId: '******',
                    accessKeySecret: '******',
                    bucket: 'ai-try-on',
                });

                let img_list = [];
                let real_name;
                async function list(dir) {
                    try {
                        let result = await client.list({
                            prefix: prefix.slice(0, -4)
                        });
                        console.log("prefix")
                        console.log(prefix)
                        console.log("result")
                        console.log(result)
                        img_list = result.objects;
                        let name_list = [];
                        for (let key in img_list){
                            name_list.push(img_list[key].name)
                        }
                        let times = name_list.map(item => parseInt(item.slice(-21,-5)));
                        let time = parseInt(prefix.slice(-16));
                        console.log("times");
                        console.log(times);
                        console.log("time");
                        console.log(time);
                        let min = 0;
                        for(let i in times){
                            if((time - times[i]) < (time - min)){
                                min = times[i];
                            }
                        }
                        real_name = name_list[times.indexOf(min)];
                        console.log("real_name");
                        console.log(real_name);

                        return real_name;
                    }catch (e) {
                        console.log(e);
                    }
                }
                list().then(res => {
                    console.log("list res");
                    console.log(res);
                    this.clothObjectKey = res;
                });
            },
            getClothImgUrl(){
                let postData = new FormData();
                postData.append("clothObjectKey", JSON.stringify(this.clothObjectKey))
                this.axios.post("http://127.0.0.1:8000/api/getCloth/", postData, {responseType: 'arraybuffer'})
                    .then(res => {
                        let clothBuffer = res.data;
                        this.clothBytes = clothBuffer
                        console.log(typeof clothBuffer)

                        let imgUrl = 'data:image/png;base64,' + btoa(new Uint8Array(clothBuffer).reduce((data, byte) => data + String.fromCharCode(byte), ''));
                        // 这里如果不清楚 new Uint8Array(data.data) 中data的指代，就看看最上面的那个图
                        this.clothImgUrl = imgUrl
                    })
                    .catch(reason => {
                        this.$message({"type":"warning", "message": reason});
                    })
            },
            toFittingRoom(){
                this.$store.commit("changeClothObjectKey", this.clothObjectKey)
                this.$router.push("/fittingRoom")
                rtc.client.leave()
            }
        },
        mounted() {
            this.watchLive();
        },
    }
</script>

<style scoped>
.watchLive{
    display: flex;
    justify-content: center;
    height: 500px;
    margin-top: 50px;
}
.liveBox{
    width: 30%;
    border-right: #797979 1px solid;
}
.live{
    width: 300px;
    height: 500px;
    border: black 1px solid;
}
.screenShot{
    width: 40%;
    text-align: center;
}
.shotCloth{
    margin: 20px auto 20px auto;
    width: 480px;
    height: 360px;
    border: #797979 1px solid;
}
span{
    margin-right: 10px;
}
.clothImg{
    width: 480px;
    height: 360px;
}
button{
    background-color: #334466;
}
</style>
<template>
    <div class="live">
        <div class="liveRoom">
            <p class="liveTitle">{{username}}的直播间</p>
            <div class="liveBox" ref="liveBox"></div>
            <div>
                <el-button type="primary" class="ctlBtn" @click="liveVideoControl">画面(开/关)</el-button>
                <el-button type="primary" class="ctlBtn" @click="liveSoundControl">声音(开/关)</el-button>
                <el-button type="primary" @click="closeTracksAndRedirect" class="ctlBtn">返回用户中心</el-button>
            </div>
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
        localAudioTrackStats: null,
        localVideoTrackStats: null,
    };
    let options = {
        // 项目的 App ID。
        appId: '',
        // 传入目标频道名。
        channel: '',
        // 生成的 Token 值。
        token: '',
        // 设置频道内的用户角色，可设为 "audience" 或 "host"
        role: "host",
        uid: null
    };
    export default {
        name: "live",
        data() {
            return {
                username: '',
            }
        },
        methods: {
            closeTracks(){
                this.axios.get("http://127.0.0.1:8000/users/stopLive/")
                    .then(res => {
                        if(res.data["msg_code"] === 100){
                            // 离开频道
                            async function leaveCall() {
                                // 销毁本地音视频轨道。
                                await rtc.client.unpublish([rtc.localAudioTrack, rtc.localVideoTrack]);
                                rtc.localAudioTrack.close();
                                rtc.localVideoTrack.close();
                                await rtc.client.leave();
                            }
                            leaveCall();
                        }else {
                            this.$message({"type": "warning", "message": res.data["message"]})
                        }
                    })
                    .catch(reason => {
                        this.$message({"type": "warning", "message": reason})
                    })
            },
            closeTracksAndRedirect(){
                this.closeTracks();
                this.$router.push("/userCenter");
            },
            startLive(){
                let meetingInfo = this.$store.state.liveInfo;
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
                    // 创建并发布本地音视频轨道
                    // 通过麦克风采集的音频创建本地音频轨道对象。
                    rtc.localAudioTrack = await AgoraRTC.createMicrophoneAudioTrack();
                    // 通过摄像头采集的视频创建本地视频轨道对象。
                    rtc.localVideoTrack = await AgoraRTC.createCameraVideoTrack();
                    // 将这些音视频轨道对象发布到频道中。
                    await rtc.client.publish([rtc.localAudioTrack, rtc.localVideoTrack]);
                    console.log("publish success!");
                    let videoContainer = document.querySelector(".liveBox");
                    console.log(videoContainer);
                    let myVideo = document.createElement("div");
                    myVideo.id = options.uid.toString();
                    myVideo.style.width = "640px";
                    myVideo.style.height = "480px";
                    videoContainer.append(myVideo);
                    rtc.localVideoTrack.play(myVideo);
                    rtc.localAudioTrack.play();
                    rtc.localAudioTrackStats = true;
                    rtc.localVideoTrackStats = true;
                }
                startBasicLive();
            },
            liveSoundControl(){
                    rtc.localAudioTrackStats = !rtc.localAudioTrackStats;
                    rtc.localAudioTrack.setEnabled(rtc.localAudioTrackStats);
            },
            liveVideoControl(){
                rtc.localVideoTrackStats = !rtc.localVideoTrackStats;
                rtc.localVideoTrack.setEnabled(rtc.localVideoTrackStats);
            }
        },
        mounted() {
            this.startLive();
        },
        beforeDestroy() {
            this.closeTracks();
        },
        watch:{
            $route:{
                handler(){
                    this.axios.get('http://127.0.0.1:8000/users/getUser').then( res => {this.username = res.data.username})
                },
                immediate: true
            }
        },
    }
</script>

<style scoped>
.live{
    display: flex;
    justify-content: space-around;
}
p{
    margin: 20px auto;
}
.liveBox{
    /*width: 300px;*/
    /*height: 500px;*/
    width: 640px;
    height: 480px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 5px;
    border: #797979 1px solid;
}
.ctlBtn{
    font-size: 10px;
}
button{
    background-color: #334466;
}
</style>
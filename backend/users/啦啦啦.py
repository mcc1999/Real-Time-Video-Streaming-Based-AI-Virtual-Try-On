startLive(){
    let meetingInfo = this.$route.params.meeting;
    options.appId = meetingInfo["appID"];
    options.channel = meetingInfo["channel"];
    options.token = meetingInfo["token"];
    options.uid = meetingInfo["uid"];

    async function startBasicLive() {
        // 创建客户端
        tc.client = AgoraRTC.createClient({ mode: "live", codec: "vp8" });
        // 设置用户角色
        rtc.client.setClientRole(options.role);
        //加入目标频道
        await rtc.client.join(options.appId, options.channel,
            options.token, options.uid);
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
        myVideo.style.width = "300px";
        myVideo.style.height = "500px";
        videoContainer.append(myVideo);
        rtc.localVideoTrack.play(myVideo);
        rtc.localAudioTrack.play();
        rtc.localAudioTrackStats = true;
        rtc.localVideoTrackStats = true;
    }
    startBasicLive();
}
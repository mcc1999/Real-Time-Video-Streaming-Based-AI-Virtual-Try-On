<template>
    <div class="fittingRoom">
        <div class="personalImg">
            <el-upload action="#" ref="upload" list-type="picture-card" :auto-upload="false" limit=1 :http-request="uploadToOSS">
                <el-button slot="trigger" type="primary" class="btn-choose">选择个人图片</el-button>
                <div slot="file" slot-scope="{file}">
                    <img class="el-upload-list__item-thumbnail" :src="file.url" alt="">
                    <span class="el-upload-list__item-actions">
                        <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
                         <i class="el-icon-zoom-in"></i>
                        </span>
                        <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleRemove(file)">
                            <i class="el-icon-delete"></i>
                        </span>
                    </span>
                </div>
                <el-button type="success" style="margin-top: 15px;margin-left:auto;margin-right:auto;display: block" @click="uploadSubmit">上传至云存储</el-button>
                <el-button type="primary" class="btn-tryOn" @click="getAITryOnClothUrl">虚拟试衣</el-button>
            </el-upload>
            <el-dialog :visible.sync="dialogVisible">
                <img width="100%" :src="dialogImageUrl" alt="">
            </el-dialog>
        </div>
        <div class="clothRoom">
            <p>试衣间
                <el-button class="backLive" size="small" @click="backLiveRoom">返回用户中心</el-button>
            </p>
            <div class="room">
                <div class="cloth">
                    <div class="clothImage"><img :src="cutClothImgUrl" alt="" class="cutCloth" style="object-fit: contain"></div>
                    <span>服饰照片</span>
                </div>
                <span class="line"></span>
                <div class="tryOn">
                    <div class="tryOnImage"><img :src="AITryOnClothUrl" alt="" class="cutCloth" style="object-fit: contain"></div>
                    <span>试衣效果</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Vue from 'vue'
    export default {
        name: "fittingRoom",
        data() {
            return {
                cutClothImgUrl: '',
                dialogImageUrl: '',
                dialogVisible: false,
                disabled: false,
                AITryOnClothUrl: '',
            }
        },
        methods: {
            getCutCloth(){
                let postData = new FormData();
                let clothObjectKey = this.$store.state.clothObjectKey
                postData.append("clothObjectKey", JSON.stringify(clothObjectKey));
                this.axios.post("http://127.0.0.1:8000/api/getCutCloth/", postData, {responseType: 'arraybuffer'})
                    .then(res => {
                        let cutClothBuffer = res.data;
                        let cutClothImgUrl = 'data:image/png;base64,' + btoa(new Uint8Array(cutClothBuffer).reduce((data, byte) => data + String.fromCharCode(byte), ''));
                        this.cutClothImgUrl = cutClothImgUrl;
                    })
                    .catch(reason => {
                        this.$message({"type":"warning", "message": reason});
                    })
            },
            handleRemove(file) {
                console.log(file);
            },
            handlePictureCardPreview(file) {
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            },
            uploadToOSS(param){
                let OSS = require('ali-oss');

                let client = new OSS({
                    // region以杭州为例（oss-cn-hangzhou），其他region按实际情况填写。
                    region: 'oss-cn-shanghai',
                    accessKeyId: 'LTAI4GBVto9H6MdfwavhqbaF',
                    accessKeySecret: 'Y30nP0NAfahdDmmLsbQbqztDIboNaY',
                    bucket: 'ai-try-on',
                });


                // 支持File对象、Blob数据以及OSS Buffer。
                const data = param.file;
                this.$store.commit('humanImageNameChange', Date.now().toString()+".jpg")
                let objectName = this.$store.state.humanImageName
                // or const data = new Blob('content');
                // or const data = new OSS.Buffer('content'));

                async function putObject () {
                    try {
                        // object-key可以自定义为文件名（例如file.txt）或目录（例如abc/test/file.txt）的形式，实现将文件上传至当前Bucket或Bucket下的指定目录。
                        let result = await client.put(objectName, data);
                        console.log(result);
                        Vue.prototype.$message({"type":"success", "message":"上传成功！"})
                    } catch (e) {
                        Vue.prototype.$message({"type":"success", "message":e})
                        console.log(e);
                    }
                }
                putObject();
            },
            uploadSubmit(){
                this.$refs.upload.submit();
            },
            backLiveRoom(){
                this.$router.push('./watchLive')
            },
            getAITryOnClothUrl(){
                this.axios.get("http://127.0.0.1:8000/api/getAICloth/", {responseType: 'arraybuffer'})
                    .then(res => {
                        let AITryOnClothUrlBuffer = res.data;
                        let AITryOnClothUrl = 'data:image/png;base64,' + btoa(new Uint8Array(AITryOnClothUrlBuffer).reduce((data, byte) => data + String.fromCharCode(byte), ''));
                        this.AITryOnClothUrl = AITryOnClothUrl;
                    })
                    .catch(reason => {
                        this.$message({"type":"warning", "message": reason});
                    })
            }
        },
        created() {
            this.getCutCloth()
        },
    }
</script>

<style scoped>
.fittingRoom{
    display: flex;
    justify-content: center;
    height: 550px;
    margin-top: 25px;
}
.personalImg{
    width: 20%;
    padding-top: 100px;
    border-right: #797979 1px solid;
}
.personalImage{
    width: 180px;
    height: 300px;
}
.clothRoom{
    width: 60%;
}
p:first-of-type{
    font-size: 50px;
    margin: 25px;
    border-bottom: #797979 1px solid;
}
.backLive{
    font-size: 10px;
}
.room{
    width: 50%;
    display: flex;
    justify-content: center;
    height: 400px;
    margin-left: auto;
    margin-right: auto;
}
.cloth{
    border-right: #797979 1px solid;
    padding: 5px 90px 50px 90px;
}
.clothImage{
    width: 180px;
    height: 300px;
    border: #797979 1px solid;
    margin-bottom: 25px;

}
.tryOn{
    width: 360px;
    padding: 5px 90px 50px 90px;
}
.tryOnImage{
    width: 180px;
    height: 300px;
    border: #797979 1px solid;
    margin-bottom: 25px;
}
span{
    font-weight: bold;
}
.line{
    width: 1px;
    height: 400px;
    background-color: #797979;
}
.cutCloth{
    width: 180px;
    height: 300px;
}
.btn-choose{
    background-color: #334466;
}
.btn-tryOn{
    margin-left: -2px;
    margin-top: 10px;
    width: 125px;
    background-color: #334466;
}
</style>
<template>
    <div>
        <img :src="this.url" alt="" class="cloth">
    </div>
</template>

<script>
    export default {
        name: "test",
        data(){
            return{
                url: ''
            }
        },
        methods:{
            download(prefix){
                const OSS = require('ali-oss');

                const client = new OSS({
                    region: 'oss-cn-shanghai',
                    accessKeyId: 'LTAI4GBVto9H6MdfwavhqbaF',
                    accessKeySecret: 'Y30nP0NAfahdDmmLsbQbqztDIboNaY',
                    bucket: 'ai-try-on',
                });

                let img_list = [];
                let real_name = '';
                async function list(dir) {
                    try {
                        let result = await client.list({
                            prefix: prefix.slice(0, -4)
                        });
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

                    }catch (e) {
                        console.log(e);
                    }
                }
                list();
                let postData = new FormData();
                postData.append("clothName", real_name);
                this.axios.post("http://127.0.0.1:8000/api/getCloth/", postData).then(res => this.url = res.data)
                console.log(this.url)
            }
        },
        mounted(){
            this.download("236524bcc74eb39bc3e68d8829fc5295_52000__uid_s_1__uid_e_video_2021032413164173");
        }
    }
</script>

<style scoped>
.cloth{
    width: 300px;
    height: 500px;
}
</style>
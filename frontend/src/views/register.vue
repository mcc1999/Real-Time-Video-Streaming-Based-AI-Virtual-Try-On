<template>
    <div class="registerForm">
        <h1>注册</h1>
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="用户名：" prop="username">
                <el-input v-model="ruleForm.username" auto-complete="off"></el-input>
            </el-form-item>
            <el-form-item label="密码：" prop="password">
                <el-input type="password" v-model="ruleForm.password" auto-complete="off" show-password></el-input>
            </el-form-item>
            <el-form-item label="确认密码：" prop="passwordConf">
                <el-input type="password" v-model="ruleForm.passwordConf" auto-complete="off" show-password></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')" class="btn-reg">注册</el-button>
                <el-button @click="toLogin">登录</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    export default {
        name: "register",
        data(){
            const validatePass = (rule, value, callback) => {
                if(!value){
                    callback(new Error('请输入密码'))
                }
                else{
                    let pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,20}$/;
                    if(!value.match(pattern)){
                        callback(new Error('密码为数字，大小写字母至少一位,长度为 8 - 20位'))
                    }
                    else {
                        callback()
                    }
                }
            }
            const validatePassConf = (rule, value, callback) => {
                if (!value) {
                    callback(new Error('请再次输入密码'))
                } else{
                    if (value !== this.ruleForm.password) {
                        callback(new Error('两次密码不一致'))
                    } else {
                        callback()
                    }
                }
            }
            return {
                ruleForm: {
                    username:'',
                    password:'',
                    passwordConf:'',
                },
                rules: {
                    username: [
                        { required: true, message: "请输入用户名", trigger: 'blur' }
                    ],
                    password: [
                        // { require: true, message: "请输入密码", trigger: 'blur' },
                        // { pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,20}$/, message: '密码为数字，小写字母，大写字母长度为 8 - 20位'}
                        { required: true },
                        { validator: validatePass, trigger: ['blur', 'change'] }
                    ],
                    passwordConf: [
                        { required: true },
                        { validator: validatePassConf, trigger: ['blur', 'change'] }
                    ],
                },
            }
        },
        methods: {
            submitForm(formName){
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let register_data = new FormData();
                        register_data.append('username', this.ruleForm.username)
                        register_data.append('password', this.ruleForm.password)
                        register_data.append('passwordConf', this.ruleForm.passwordConf)
                        this.axios.post('http://127.0.0.1:8000/users/register/', register_data)
                            .then(res => {
                                if(res.data["msg_code"] === 100){
                                    this.$message({"type": "success", "message": res.data.message})
                                    this.$router.push('/login')
                                    console.log('Form' + formName + 'submit!');
                                } else{
                                    this.$message.error({"type": "warning", "message": res.data.message})
                                }
                            })
                            .catch(res => {
                                console.log("error submit!")
                                return false
                            })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            toLogin(){
                this.$router.push('/login')
            }
        }
    }
</script>

<style scoped>
.registerForm{
    width: 400px;
    margin: 100px auto;
    padding: 20px;
    background: #ffffff;
    box-shadow: 10px 10px 10px #dcdfe6;
    border-radius: 5%;
    border: 1px solid #dcdfe6;
    opacity: 0.9;
}
h1{
    color: black;
    font-weight: bold;
}
.btn-reg{
    background-color: #334466;
}
</style>
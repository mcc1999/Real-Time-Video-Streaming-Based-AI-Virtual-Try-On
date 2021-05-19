<template>
    <div class="loginForm">
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
            <h1>登录</h1>
            <el-form-item label="用户名：" prop="username">
                <el-input v-model="ruleForm.username" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="密码：" prop="password">
                <el-input type="password" v-model="ruleForm.password" auto-complete="off" show-password></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')" class="btn-login">登录</el-button>
                <el-button @click="toRegister">注册</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    export default {
        name: 'login',
        data() {
            return {
                ruleForm: {
                    username: '',
                    password: '',
                },
                rules: {
                    username: [
                        { required: true, message: '用户名不能为空', trigger: 'blur' },
                    ],
                    password: [
                        { required: true, message: '密码不能为空', trigger: 'blur' },
                    ],
                }
            };
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let login_data = new FormData();
                        login_data.append('username', this.ruleForm.username)
                        login_data.append('password', this.ruleForm.password)
                        this.axios.post('http://127.0.0.1:8000/users/login/', login_data)
                            .then(res => {
                                if(res.data["msg_code"] === 100){
                                    this.$message({"type": "success", "message": res.data.message})
                                    this.$router.push('/userCenter')
                                    console.log('Form' + formName + 'submit!');
                                } else{
                                    this.$message({"type": "warning", "message": res.data.message})
                                }
                            })
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            toRegister() {
                this.$router.push('/register')
            }
        },
    }
</script>

<style scoped>
.loginForm{
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
    color: #000000;
    font-weight: bold;
}
.btn-login{
    background-color: #334466;
}
</style>
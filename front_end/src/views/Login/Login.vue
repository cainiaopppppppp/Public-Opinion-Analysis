<!-- src/views/Login/Login.vue -->
<template>
  <el-card class="box-card">
    <h1 class="mb-3">登录</h1>

    <el-form class="form">
      <el-form-item label="用户名">
        <el-input v-model="username" placeholder="Username" />
      </el-form-item>

      <el-form-item label="密码">
        <el-input v-model="password" type="password" placeholder="Password" />
      </el-form-item>

      <el-row justify="space-between">
        <el-col :span="12">
          <router-link to="/register">注册</router-link>
        </el-col>

        <el-col :span="12">
          <router-link to="/forget">忘记密码</router-link>
        </el-col>
      </el-row>

      <el-button @click="onLogin" class="login-btn" type="primary" round>登录</el-button>
    </el-form>

  </el-card>
</template>

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { login } from '@/apis/login'
import { useUserStore } from '../../stores/stores'
import pinia from '../../stores/index.js'
const user = useUserStore(pinia)
import { storeToRefs } from 'pinia'
import jwtDecode from 'jwt-decode';

function handleLoginSuccess(user_id, user_uid, username) {
  user.isLoggedIn = true
  user.id = user_id
  user.uid = user_uid
  user.username = username
}
export default {

  methods: {


    onLoginFailed() {
      alert('登录失败,请重试')
    },

    async onLogin() {
      const data = {
        username: this.username,
        password: this.password
      }

      function err_reflect(mes) {
        ElMessage({
          message: mes,
          type: 'fail'
        })
      }

      try {
        const response = await login(data)
        // 获取响应结果
        const res = response.data
        console.log(res)
        if (res.status) {
          let token = res.token
          // console.log(token)
          const decoded = jwtDecode(token)
          // console.log(decoded)
          const isConfirm = confirm('登录成功,确认后跳转首页?')

          if (isConfirm) {
            handleLoginSuccess(decoded.user_id, decoded.user_uid, decoded.username)
            console.log(user.isLoggedIn)
            this.$router.push('/')
          } // 登录成功后跳转首页
        } else {
          if (res.message.password == "密码格式错误") {
            err_reflect("密码格式错误")
          } else if (res.message == "wrong password") {
            err_reflect("用户名或密码错误")
          }
        }

      } catch (err) {
        // 登录失败,显示错误
        console.error(err)
        this.onLoginFailed()
      }
    }
  },

  setup() {
    const username = ref('')
    const password = ref('')

    return {
      username,
      password
    }
  }
}
</script>

<style>
.box-card {
  width: 480px;
  margin: 0 auto;
}

.login-btn {
  width: 100%;
  margin-top: 12px;
}
</style>
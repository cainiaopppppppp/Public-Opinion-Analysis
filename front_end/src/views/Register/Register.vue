<!-- src/views/Register/Register.vue -->
<template>
  <el-card class="box-card">
    <h1 class="mb-3">Register</h1>

    <el-form class="form">

      <el-form-item label="用户名">
        <el-input v-model="username" placeholder="Username"/>
      </el-form-item>

      <el-form-item label="邮箱">
        <el-input v-model="email" placeholder="Email"/>
      </el-form-item>
      
      <el-form-item label="密码">
        <el-input v-model="password" type="password" placeholder="Password"/>
      </el-form-item>
      
      <el-form-item label="再次输入密码">
        <el-input v-model="confirmPassword" type="password" placeholder="Confirm Password"/>
      </el-form-item>

      <el-row :gutter="20">
        <el-col :span="24">
          <router-link to="/login">已有账号,点击登录</router-link>
        </el-col>

        <el-col :span="24">
          <el-row justify="center">
            <el-button class="register-btn" type="primary" round @click="onRegister">注册</el-button>
          </el-row>
        </el-col>

      </el-row>

    </el-form>

  </el-card>
</template>

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { register } from '@/apis/register'
export default {

  methods: {
    async onRegister() {
      if (this.password !== this.confirmPassword) {
        ElMessage.error('两次输入密码不一致')
        return
      }
      
      const data = {
        username: this.username,
        email: this.email, 
        password: this.password
      }

      try {
        await register(data)
        
        // 注册成功
        ElMessage.success('注册成功')
        this.$router.push('/login')

      } catch(err) {
        
        // 注册失败
        ElMessage.error(err.message || '注册失败')     
      }
    }
  },

  setup() {
    const username=ref('')
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')

    return {
      username,
      email,
      password,
      confirmPassword
    }
  }
}
</script>

<style>
/* 样式 */
</style>
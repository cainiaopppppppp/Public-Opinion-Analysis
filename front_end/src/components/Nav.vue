<!-- /src/components/Nav.vue -->
<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/stores'
import pinia from '../stores/index.js'

const router = useRouter()

const user = useUserStore(pinia)

function reloadPage() {
    router.replace(router.currentRoute.value.fullPath)
}
function toggleLogin() {
    user.isLoggedIn = !user.isLoggedIn
    // isLoggedIn = user.isLoggedIn
    reloadPage()
}
watch(user.isLoggedIn, (newValue, oldValue) => {
    if (newValue !== oldValue) {
        reloadPage()
    }
})
</script>
<template>
    <nav>
        <div class="nav-left">
            <img src="" class="logo" />
            <span class="app-name">话题-观点图谱</span>
        </div>

        <div class="nav-right">
            <template v-if="user.isLoggedIn">
                <router-link to="/">主页</router-link>
                <router-link to="/charts">词云表</router-link>
                <!-- <router-link to="/graphvisual">图谱可视化</router-link> -->
                <router-link to="/opinion">已有图谱可视化</router-link>
                <router-link to="/text">实时分析</router-link>
                <router-link to="/" @click="toggleLogin">登出</router-link>
            </template>

            <template v-else>
                <router-link to="/">主页</router-link>
                <router-link to="/login">登录</router-link>
                <router-link to="/register">注册</router-link>
            </template>
        </div>
    </nav>
</template>
  
<style scoped>
nav {
    /* position: absolute; */
    position: fixed;
    top: 0;
    width: 100%;
    top: 0px;
    left: 0;
    right: 0;
    z-index: 999;
    display: flex;
    /* align-items: stretch; */
    justify-content: space-between;
    /* align-items: center; */
    background-color: #333;
    color: #fff;
    padding: 1rem;
    /* width: 100vw; */
}

.logo {
    width: 5rem;
    margin-right: 5rem;
    display: inline-block;
}

.app-name {
    font-weight: bold;
    font-size: 1.5rem;
    display: inline-block;
}

.nav-right {
    display: flex;
    align-items: center;
}

.nav-right a {
    color: #fff;
    text-decoration: none;
    margin-right: 1rem;
}

@media (max-width: 600px) {
    nav {
        flex-direction: column;
    }

    .nav-left,
    .nav-right {
        margin-bottom: 0.5rem;
    }
}
</style>
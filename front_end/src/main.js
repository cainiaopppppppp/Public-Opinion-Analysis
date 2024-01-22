// /src/main.js
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)
app.use(ElementPlus)
// app.use(ElementPlus)
app.use(router)

app.mount('#app')

// global
app.directive('image_lazy', {
    mounted(el, binding) {
        console.log(el, binding.value)
    }
})
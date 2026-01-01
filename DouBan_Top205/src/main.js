import './style.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
const pinia = createPinia()
import * as echarts from 'echarts'
import router from './router'

const app = createApp(App)
app.config.globalProperties.$echarts = echarts
app.use(ElementPlus)
app.use(router)
app.use(pinia)
app.mount('#app')

import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import * as echarts from 'echarts'
import router from './router'

const app = createApp(App)
app.config.globalProperties.$echarts = echarts
app.use(router)
app.mount('#app')

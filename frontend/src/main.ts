import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import Vue3Toastify, { type ToastContainerOptions } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import './assets/main.css'
import dayjs from 'dayjs'
import weekOfYear from 'dayjs/plugin/weekOfYear'
import isoWeek from 'dayjs/plugin/isoWeek'
import isToday from 'dayjs/plugin/isToday'
import isYesterday from 'dayjs/plugin/isYesterday'
dayjs.extend(weekOfYear)
dayjs.extend(isoWeek)
dayjs.extend(isToday)
dayjs.extend(isYesterday)

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(Vue3Toastify, {
  autoClose: 2500,
  position: 'top-center',
  style: { fontFamily: 'Nunito, sans-serif' },
} as ToastContainerOptions)

app.mount('#app')

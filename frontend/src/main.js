import { createApp } from "vue"
import { createPinia } from "pinia"

import App from "./App.vue"
import router from "./router"

import api from "./services/api"

import { useAuthStore } from "./stores/auth"
import { useFlashStore } from "./stores/flash"

import "./assets/styles/global.css"

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

const authStore = useAuthStore(pinia)
const flash = useFlashStore(pinia)

if (!authStore.initialized) {
    await authStore.fetchCurrentUser()
}

api.interceptors.response.use(

    response => response,

    async error => {

        if (error.response?.status === 401 && authStore.isLoggedIn) {

            await authStore.handleSessionExpired(error.response.data?.message)

        }

        return Promise.reject(error)
    
    }
)

app.mount("#app")

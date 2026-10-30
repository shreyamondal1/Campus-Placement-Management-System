import { defineStore } from "pinia"
import { ref, computed } from "vue"

import router from "../router"
import { useFlashStore } from "./flash"
import { loginUser, logoutUser, getCurrentUser } from "../services/auth"

export const useAuthStore = defineStore("auth", () => {

    const flash = useFlashStore()
    
    const user = ref(null)
    const initialized = ref(false)
    const handlingSessionExpiry = ref(false)

    const isLoggedIn = computed(() => user.value !== null)

    async function login(usernameOrEmail, password, role) {

        const response = await loginUser({
            username_or_email: usernameOrEmail,
            password: password,
            role: role
        })

        user.value = response.data.user

        flash.success(response.data.message, 1000)

        await new Promise(resolve => setTimeout(resolve, 1000))

        return user.value
    }

    async function logout() {

        const response = await logoutUser()

        flash.success(response.data.message)

        user.value = null
    }

    async function fetchCurrentUser(force = false) {

        if (initialized.value && !force) {

            return
        
        }

        try {

            const response = await getCurrentUser()

            user.value = response.data

            return true
        
        }
        catch (error) {

            if (error.response?.status === 401) {

                user.value = null

                return false
            
            }
            else {
            
                throw error
            
            }
        }
        finally {
        
            initialized.value = true
        
        }
    }

    async function handleSessionExpired(message) {

        if (handlingSessionExpiry.value) {

            return
        
        }

        handlingSessionExpiry.value = true

        const role = user.value?.role

        flash.error(message || "Session expired. Please log in again.", 1000)

        await new Promise(resolve => setTimeout(resolve, 1000))

        user.value = null

        await router.push({name: `${role.toLowerCase()}-login`})
}

    return {
        user,
        initialized,
        isLoggedIn,
        login,
        logout,
        fetchCurrentUser,
        handleSessionExpired
    }
})

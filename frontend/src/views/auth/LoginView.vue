<template>
    <div class="container py-5">
        <h1 class="text-center mb-4"> {{ loginRole }} Sign-in </h1>
        <div class="row justify-content-center align-items-center">
            <div class="col-lg-5 col-md-7 col-sm-9">
                <div class="card shadow-sm">
                    <div class="card-body p-4">
                        <form v-on:submit.prevent="login">
                            <div class="mb-3">
                                <label for="username-or-email" class="form-label">Username or Email</label>
                                <input id="username-or-email" v-model="usernameOrEmail" type="text" class="form-control" required>
                            </div>
                            <div class="mb-3"> 
                                <label for="password" class="form-label">Password</label>
                                <input id="password" v-model="password" type="password" class="form-control" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100" v-bind:disabled="loading"> {{ loading ? "Logging in..." : "Login" }} </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"

import { useAuthStore } from "../../stores/auth"
import { useFlashStore } from "../../stores/flash"

const flash = useFlashStore()

const route = useRoute()
const router = useRouter()

const authStore = useAuthStore()

const loginRole = route.meta.loginRole

const usernameOrEmail = ref("")
const password = ref("")

const loading = ref(false)

async function login() {

    loading.value = true

    try {
        const result = await authStore.login(
            usernameOrEmail.value,
            password.value,
            loginRole
        )

        await router.push({name: `${result.role.toLowerCase()}-dashboard`})
    }
    catch (error) {
        flash.error(error.response?.data?.message || "Login failed.")
    }
    finally {
        loading.value = false
    }
}
</script>

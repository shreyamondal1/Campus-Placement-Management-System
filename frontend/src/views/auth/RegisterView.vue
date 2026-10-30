<template>
    <div class="container py-5">
        <h1 class="text-center mb-4"> {{ registrationRole }} Sign-up </h1>
        <div class="row justify-content-center align-items-center">
            <div class="col-lg-5 col-md-7 col-sm-9">
                <div class="card shadow-sm">
                    <div class="card-body p-4">
                        <form v-on:submit.prevent="register">
                            <div class="mb-3">
                                <label for="username" class="form-label">Username</label>
                                <input id="username" v-model="username" type="text" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input id="email" v-model="email" type="email" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Password</label>
                                <input id="password" v-model="password" type="password" class="form-control" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100" v-bind:disabled="loading"> {{ loading ? "Registering..." : "Register" }} </button>
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

import { registerUser } from "../../services/auth"
import { useFlashStore } from "../../stores/flash"

const flash = useFlashStore()

const route = useRoute()
const router = useRouter()

const registrationRole = route.meta.registrationRole

const username = ref("")
const email = ref("")
const password = ref("")

const loading = ref(false)

async function register() {

    loading.value = true

    try {
        const response = await registerUser({
            username: username.value,
            email: email.value,
            password: password.value,
            role: registrationRole
        })

        flash.success(response.data.message, 1000)

        await new Promise(resolve => setTimeout(resolve, 1000))

        await router.push({name: `${registrationRole.toLowerCase()}-login`})
    }
    catch (error) {
        flash.error(error.response?.data?.message || "Registration failed.")
    }
    finally {
        loading.value = false
    }
}
</script>

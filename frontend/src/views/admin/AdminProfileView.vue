<template>
    <div class="container py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-semibold mb-1">Profile</h2>
            <button class="btn btn-primary" type="button" v-on:click="exportData" v-bind:disabled="exporting"><i class="bi bi-download me-2"></i> {{ exporting ? "Generating..." : "Export Data" }} </button>
        </div>
        <div v-if="loading" class="text-center py-5"><div class="spinner-border"></div></div>
        <div v-else-if="error" class="alert alert-danger"> {{ error }} </div>
        <div v-else>
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="fw-semibold mb-4">Account Information</h5>
                    <div v-if="!editing">
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Username</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.username }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Email</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.email }} </p></div>
                        </div>
                        <div class="mt-4">
                            <button type="button" class="btn btn-primary" v-on:click="startEditing"><i class="bi bi-pencil me-2"></i>Edit Profile</button>
                        </div>
                    </div>
                    <form v-else v-on:submit.prevent="updateProfile">
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Username</label>
                            <div class="col-sm-9"><input v-model="editProfile.username" type="text" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Email</label>
                            <div class="col-sm-9"><input v-model="editProfile.email" type="email" class="form-control" required></div>
                        </div>
                        <div class="row mb-4">
                            <label class="col-sm-3 col-form-label fw-semibold">Password</label>
                            <div class="col-sm-9"><input v-model="editProfile.password" type="password" class="form-control" required></div>
                        </div>
                        <button type="submit" class="btn btn-success" v-bind:disabled="saving"> {{ saving ? "Saving..." : "Save Changes" }} </button>
                        <button type="button" class="btn btn-secondary ms-2" v-on:click="cancelEditing" v-bind:disabled="saving">Cancel</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue"

import { getAdminProfile, updateAdminProfile, exportAdminProfile, getAdminInboxStatus } from "../../services/admin"

import { useToastStore } from "../../stores/toast"

const toast = useToastStore()

const profile = ref({
    username: "",
    email: ""
})

const editProfile = ref({
    username: "",
    email: "",
    password: ""
})

const error = ref("")
const loading = ref(false)
const editing = ref(false)
const saving = ref(false)
const exporting = ref(false)

const successMessage = ref("")
const errorMessage = ref("")

let notificationInterval = null

async function loadProfile() {

    loading.value = true
    error.value = ""

    try {

        const data = await getAdminProfile()

        profile.value.username = data.username
        profile.value.email = data.email

    } catch (err) {

        error.value = err.response?.data?.message || "Failed to load profile."

    } finally {

        loading.value = false

    }

}

function startEditing() {

    editProfile.value = {
        username: profile.value.username,
        email: profile.value.email,
        password: ""
    }

    successMessage.value = ""
    errorMessage.value = ""
    editing.value = true

}

function cancelEditing() {

    editing.value = false
    errorMessage.value = ""

}

async function updateProfile() {

    saving.value = true
    successMessage.value = ""
    errorMessage.value = ""

    try {

        const data = await updateAdminProfile({
            username: editProfile.value.username,
            email: editProfile.value.email,
            password: editProfile.value.password
        })

        profile.value.username = data.username
        profile.value.email = data.email

        editing.value = false

        successMessage.value = "Profile updated successfully."

        toast.completion(successMessage)

    } catch (err) {

        errorMessage.value = err.response?.data?.message || "Failed to update profile."

        toast.completion(errorMessage)

    } finally {

        saving.value = false
    
    }

}

async function exportData() {

    exporting.value = true
    successMessage.value = ""
    errorMessage.value = ""

    try {

        const data = await exportAdminProfile()

        successMessage.value = data.message || "Export generation started. You will be notified when it is ready."

        toast.completion(successMessage)

    } catch (err) {

        errorMessage.value = err.response?.data?.message || "Failed to start export."

        toast.completion(errorMessage)

    } finally {

        exporting.value = false

    }

}

async function checkNotificationStatus() {

    try {

        const status = await getAdminInboxStatus()

        if (status.task_completed) {

            toast.completion(status.message)

        }

    } catch (err) {

        error.value = err.response?.data?.message || "Failed to check notification status"

    }

}

onMounted(() => {

    loadProfile()

    checkNotificationStatus()

    notificationInterval = setInterval(checkNotificationStatus, 100)

})

onUnmounted(() => {

    clearInterval(notificationInterval)

})

</script>

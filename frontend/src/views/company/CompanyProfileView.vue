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
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.email }}</p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Name</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.name }}</p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Description</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.description || "-" }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Industry</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.industry || "-" }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Type</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.type || "-" }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Website</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.website }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">HR Contact Name</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.hr_contact_name }} </p></div></div>
                        <div class="row mb-4">
                            <label class="col-sm-3 col-form-label fw-semibold">HR Contact Number</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.hr_contact_number }} </p></div>
                        </div>
                        <div class="mt-4">
                            <button type="button" class="btn btn-primary" v-on:click="startEditing"><i class="bi bi-pencil me-2"></i>Edit Profile</button>
                            <button type="button" class="btn btn-danger ms-2" v-on:click="deleteProfile" v-bind:disabled="deleting"><i class="bi bi-trash me-2"></i> {{ deleting ? "Deleting..." : "Delete Profile" }} </button>
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
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Name</label>
                            <div class="col-sm-9"><input v-model="editProfile.name" type="text" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Description</label>
                            <div class="col-sm-9"><textarea v-model="editProfile.description" class="form-control" rows="3"></textarea></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Industry</label>
                            <div class="col-sm-9"><input v-model="editProfile.industry" type="text" class="form-control"></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Type</label>
                            <div class="col-sm-9"><input v-model="editProfile.type" type="text" class="form-control"></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Website</label>
                            <div class="col-sm-9"><input v-model="editProfile.website" type="url" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">HR Contact Name</label>
                            <div class="col-sm-9"><input v-model="editProfile.hr_contact_name" type="text" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">HR Contact Number</label>
                            <div class="col-sm-9"><input v-model="editProfile.hr_contact_number" type="text" class="form-control" required ></div>
                        </div>
                        <div class="row mb-4">
                            <label class="col-sm-3 col-form-label fw-semibold">Password</label>
                            <div class="col-sm-9"><input v-model="editProfile.password" type="password" class="form-control" required></div>
                        </div>
                        <button type="submit" class="btn btn-success" v-bind:disabled="saving"> {{ saving ? "Saving..." : "Save Changes" }} </button>
                        <button type="button" class="btn btn-secondary ms-2" v-on:click="cancelEditing" v-bind:disabled="saving">Cancel</button>
                    </form>
                    <div v-if="showConfirm" class="modal fade show" style="display:block; background-color:rgba(0,0,0,.5);">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Confirm Action</h5>
                                </div>
                                <div class="modal-body"> {{ confirmMessage }} </div>
                                <div class="modal-footer">
                                    <button class="btn btn-success" v-on:click="cancelAction">Cancel</button>
                                    <button class="btn btn-danger" v-on:click="confirmAction">Confirm</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"

import { getCompanyProfile, updateCompanyProfile, deleteCompanyProfile, exportCompanyProfile, getCompanyInboxStatus } from "../../services/company"

import { useToastStore } from "../../stores/toast"

const router = useRouter()
const toast = useToastStore()

const profile = ref({
    username: "",
    email: "",
    name: "",
    description: "",
    industry: "",
    type: "",
    website: "",
    hr_contact_name: "",
    hr_contact_number: ""
})

const editProfile = ref({
    username: "",
    email: "",
    password: "",
    name: "",
    description: "",
    industry: "",
    type: "",
    website: "",
    hr_contact_name: "",
    hr_contact_number: ""
})

const error = ref("")
const loading = ref(false)
const editing = ref(false)
const saving = ref(false)
const exporting = ref(false)
const deleting = ref(false)

const successMessage = ref("")
const errorMessage = ref("")

let notificationInterval = null

const showConfirm = ref(false)
const confirmMessage = ref("")
const pendingAction = ref(null)

async function loadProfile() {

    loading.value = true
    error.value = ""

    try {

        const data = await getCompanyProfile()

        profile.value = {
            username: data.username,
            email: data.email,
            name: data.name,
            description: data.description,
            industry: data.industry,
            type: data.type,
            website: data.website,
            hr_contact_name: data.hr_contact_name,
            hr_contact_number: data.hr_contact_number
        }

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
        password: "",
        name: profile.value.name,
        description: profile.value.description || "",
        industry: profile.value.industry || "",
        type: profile.value.type || "",
        website: profile.value.website,
        hr_contact_name: profile.value.hr_contact_name,
        hr_contact_number: profile.value.hr_contact_number
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

        const data = await updateCompanyProfile({
            username: editProfile.value.username,
            email: editProfile.value.email,
            password: editProfile.value.password,
            name: editProfile.value.name,
            description: editProfile.value.description || null,
            industry: editProfile.value.industry || null,
            type: editProfile.value.type || null,
            website: editProfile.value.website,
            hr_contact_name: editProfile.value.hr_contact_name,
            hr_contact_number: editProfile.value.hr_contact_number
        })

        profile.value = {
            username: data.username,
            email: data.email,
            name: data.name,
            description: data.description,
            industry: data.industry,
            type: data.type,
            website: data.website,
            hr_contact_name: data.hr_contact_name,
            hr_contact_number: data.hr_contact_number
        }

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

        const data = await exportCompanyProfile()

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

        const status = await getCompanyInboxStatus()

        if (status.task_completed) {

            toast.completion(status.message)

        }

    } catch (err) {

        error.value = err.response?.data?.message || "Failed to check notification status"

    }

}

function deleteProfile() {

    openConfirm("Are you sure you want to delete your account?", confirmDeleteProfile)

}

async function confirmDeleteProfile() {

    deleting.value = true
    successMessage.value = ""
    errorMessage.value = ""

    try {

        await deleteCompanyProfile()

        await router.push({name: "home"})

    } catch (err) {

        errorMessage.value = err.response?.data?.message || "Failed to delete profile."

        toast.completion(errorMessage)

    } finally {

        deleting.value = false

    }

}

function openConfirm(message, action) {

    showConfirm.value = true
    confirmMessage.value = message
    pendingAction.value = action

}

async function confirmAction() {

    showConfirm.value = false

    if (pendingAction.value) {
        await pendingAction.value()
        pendingAction.value = null
    }

}

function cancelAction() {

    showConfirm.value = false
    pendingAction.value = null

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

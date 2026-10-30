<script setup>
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"

import ApplicationSection from "../../components/sections/ApplicationSection.vue"
import StudentSection from "../../components/sections/StudentSection.vue"
import DriveSection from "../../components/sections/DriveSection.vue"
import CompanySection from "../../components/sections/CompanySection.vue"

import { getAdminApplicationData } from "../../services/admin"

const route = useRoute()

const applicationId = route.params.applicationId

const applicationData = ref(null)
const loading = ref(false)
const error = ref("")

async function loadApplicationData() {

    loading.value = true
    error.value = ""

    try {
        applicationData.value = await getAdminApplicationData(applicationId)
    }

    catch (err) {
        error.value = err.response?.data?.message || "Failed to load application data."
    }

    finally {
        loading.value = false
    }

}

onMounted(loadApplicationData)
</script>

<template>
    <div class="container py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold mb-2">Application</h2>
            <div v-if="applicationData" class="text-muted">
                 {{ applicationData.student.name }} <span class="mx-2">|</span> {{ applicationData.drive.job_title }} <span class="mx-2">|</span> {{ applicationData.company.name }} 
            </div>
        </div>
        <div v-if="loading" class="text-center py-5"><div class="spinner-border"></div></div>
        <div v-else-if="error" class="alert alert-danger"> {{ error }} </div>
        <div v-else-if="applicationData">
            <ApplicationSection
                v-bind:application="applicationData.application"
                mode="admin"
            />
            <StudentSection
                v-bind:student="applicationData.student" class="mt-4"
                mode="admin"
            />
            <DriveSection
                v-bind:drive="applicationData.drive" class="mt-4"
                mode="admin"
            />
            <CompanySection
                v-bind:company="applicationData.company" class="mt-4"
                mode="admin"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"

import ApplicationSection from "../../components/sections/ApplicationSection.vue"
import DriveSection from "../../components/sections/DriveSection.vue"
import CompanySection from "../../components/sections/CompanySection.vue"

import { getStudentCompanyDriveData } from "../../services/student"

const route = useRoute()

const companyId = route.params.companyId
const driveId = route.params.driveId

const driveData = ref(null)
const loading = ref(false)
const error = ref("")

async function loadDriveData() {

    loading.value = true
    error.value = ""

    try {
        driveData.value = await getStudentCompanyDriveData(companyId, driveId)
    }

    catch (err) {
        error.value = err.response?.data?.message || "Failed to load drive data."
    }

    finally {
        loading.value = false
    }

}

onMounted(loadDriveData)
</script>

<template>
    <div class="container py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold mb-2">Drive</h2>
            <div v-if="driveData" class="text-muted">
                 {{ driveData.drive.job_title }} <span class="mx-2">|</span> {{ driveData.company.name }} 
            </div>
        </div>
        <div v-if="loading" class="text-center py-5"><div class="spinner-border"></div></div>
        <div v-else-if="error" class="alert alert-danger"> {{ error }} </div>
        <div v-else-if="driveData">
            <ApplicationSection
                v-bind:application="driveData.application"
                mode="student"
            />
            <DriveSection
                v-bind:drive="driveData.drive" class="mt-4"
                mode="student"
            />
            <CompanySection
                v-bind:company="driveData.company" class="mt-4"
                mode="student"
            />
        </div>
    </div>
</template>

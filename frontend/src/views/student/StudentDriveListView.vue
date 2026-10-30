<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"

import { useToastStore } from "../../stores/toast"

import DriveCard from "../../components/cards/DriveCard.vue"

import { getStudentCompanyDrives, studentApplyDrive, studentWithdrawDrive } from "../../services/student"

const router = useRouter()
const route = useRoute()

const toast = useToastStore()

const companyId = route.params.companyId

const drives = ref([])
const loading = ref(false)
const error = ref("")

const search = ref("")
const eligibleStatusFilter = ref("")
const driveStatusFilter = ref("")
const applicationStatusFilter = ref("")

const filteredDrives = computed(() => {

    return drives.value.filter(drive => {

        const matchesSearch = drive.job_title.toLowerCase().includes(search.value.toLowerCase())

        const matchesEligibleStatus = !eligibleStatusFilter.value || drive.eligible_status === eligibleStatusFilter.value

        const matchesDriveStatus = !driveStatusFilter.value || drive.drive_status === driveStatusFilter.value

        const matchesApplicationStatus = applicationStatusFilter.value === "" || drive.application_exists === applicationStatusFilter.value

        return (
            matchesSearch &&
            matchesEligibleStatus &&
            matchesDriveStatus &&
            matchesApplicationStatus
            
        )

    })

})

const showConfirm = ref(false)
const confirmMessage = ref("")
const pendingAction = ref(null)

async function loadDrives() {

    loading.value = true
    error.value = ""

    try {
        drives.value = await getStudentCompanyDrives(companyId)
    }

    catch (err) {
        error.value = err.response?.data?.message || "Failed to load drives."
    }

    finally {
        loading.value = false
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

function viewDrive(driveId) {
    router.push({name: "student-company-drive-detail", params: {companyId: companyId, driveId: driveId}})
}

async function applyDrive(driveId) {

    openConfirm("Are you sure you want to apply for this drive?",
        async () => {
            try {
                const response = await studentApplyDrive(driveId)
                toast.action(response.message)
                await loadDrives()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function withdrawDrive(driveId) {

    openConfirm("Are you sure you want to withdraw this application?",
        async () => {
            try {
                const response = await studentWithdrawDrive(driveId)
                toast.action(response.message)
                await loadDrives()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

onMounted(loadDrives)
</script>

<template>
    <div class="container py-4">
        <h2 class="fw-bold mb-4">Drives</h2>
        <div v-if="loading" class="text-center py-5"><div class="spinner-border"></div></div>
        <div v-else-if="error" class="alert alert-danger"> {{ error }} </div>
        <div v-else>
            <div class="row mb-4">
                <div class="col-md-6">
                    <input v-model="search" type="text" class="form-control" placeholder="Search by Job Title">
                </div>
                <div class="col-md-2">
                    <select v-model="eligibleStatusFilter" class="form-select">
                        <option value="">Eligibility Status</option>
                        <option>Eligible</option>
                        <option>Not Eligible</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <select v-model="driveStatusFilter" class="form-select">
                        <option value="">Drive Status</option>
                        <option>Upcoming</option>
                        <option>Ongoing</option>
                        <option>Closed</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <select v-model="applicationStatusFilter" class="form-select">
                        <option value="">Application Status</option>
                        <option v-bind:value="true">Applied</option>
                        <option v-bind:value="false">Not Applied</option>
                    </select>
                </div>
            </div>
            <div class="row g-4">
                <div class="col-lg-6" v-for="drive in filteredDrives" v-bind:key="drive.id">
                    <DriveCard
                        v-bind:drive="drive"
                        mode="student"
                        v-on:view="viewDrive"
                        v-on:apply="applyDrive"
                        v-on:withdraw="withdrawDrive"
                    />
                </div>
                <div v-if="filteredDrives.length === 0" class="text-center py-5 text-muted">No drives found.</div>
            </div>
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
</template>

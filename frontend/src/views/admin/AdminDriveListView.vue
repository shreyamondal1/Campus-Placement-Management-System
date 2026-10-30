<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"

import { useToastStore } from "../../stores/toast"

import DriveCard from "../../components/cards/DriveCard.vue"

import { getAdminCompanyDrives, adminApproveDrive, adminRejectDrive, adminReapproveDrive } from "../../services/admin"

const router = useRouter()
const route = useRoute()

const toast = useToastStore()

const companyId = route.params.companyId

const drives = ref([])
const loading = ref(false)
const error = ref("")

const search = ref("")
const approvalStatusFilter = ref("")
const driveStatusFilter = ref("")

const filteredDrives = computed(() => {

    return drives.value.filter(drive => {

        const matchesSearch = drive.job_title.toLowerCase().includes(search.value.toLowerCase())

        const matchesApprovalStatus = !approvalStatusFilter.value || drive.approval_status === approvalStatusFilter.value

        const matchesDriveStatus = !driveStatusFilter.value || drive.drive_status === driveStatusFilter.value

        return (
            matchesSearch &&
            matchesApprovalStatus &&
            matchesDriveStatus
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
        drives.value = await getAdminCompanyDrives(companyId)
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
    router.push({name: "admin-company-drive-application-list", params: {companyId: companyId, driveId: driveId}})
}

async function approveDrive(driveId) {

    openConfirm("Are you sure you want to approve this drive?",
        async () => {
            try {
                const response = await adminApproveDrive(driveId)
                toast.action(response.message)
                await loadDrives()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function rejectDrive(driveId) {

    openConfirm("Are you sure you want to reject this drive?",
        async () => {
            try {
                const response = await adminRejectDrive(driveId)
                toast.action(response.message)
                await loadDrives()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function reapproveDrive(driveId) {

    openConfirm("Are you sure you want to reapprove this drive?",
        async () => {
            try {
                const response = await adminReapproveDrive(driveId)
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
                <div class="col-md-3">
                    <select v-model="approvalStatusFilter" class="form-select">
                        <option value="">Approval Status</option>
                        <option>Pending</option>
                        <option>Approved</option>
                        <option>Rejected</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <select v-model="driveStatusFilter" class="form-select">
                        <option value="">Drive Status</option>
                        <option>Upcoming</option>
                        <option>Ongoing</option>
                        <option>Closed</option>
                    </select>
                </div>
            </div>
            <div class="row g-4">
                <div class="col-lg-6" v-for="drive in filteredDrives" v-bind:key="drive.id">
                    <DriveCard
                        v-bind:drive="drive"
                        mode="admin"
                        v-on:view="viewDrive"
                        v-on:approve="approveDrive"
                        v-on:reject="rejectDrive"
                        v-on:reapprove="reapproveDrive"
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

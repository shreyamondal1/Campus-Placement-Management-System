<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"

import { useToastStore } from "../../stores/toast"

import DriveCard from "../../components/cards/DriveCard.vue"

import { getCompanyDrives, companyCreateDrive, companyUpdateDrive, companyDeleteDrive } from "../../services/company"

const router = useRouter()

const toast = useToastStore()

const drives = ref([])
const loading = ref(false)
const error = ref("")

const search = ref("")
const approvalStatusFilter = ref("")
const driveStatusFilter = ref("")

const showForm = ref(false)
const isEditing = ref(false)
const editingDriveId = ref(null)

const form = ref({
    job_title: "",
    job_description: "",
    job_location: "",
    job_type: "",
    job_mode: "",
    salary_package: "",
    eligibility_criteria: "",
    minimum_cgpa: "",
    application_start: "",
    application_deadline: ""
})

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
        drives.value = await getCompanyDrives()
    }

    catch (err) {
        error.value = err.response?.data?.message || "Failed to load drives."
    }

    finally {
        loading.value = false
    }

}

function newDrive() {

    showForm.value = true
    isEditing.value = false
    editingDriveId.value = null

    form.value = {
        job_title: "",
        job_description: "",
        job_location: "",
        job_type: "",
        job_mode: "",
        salary_package: "",
        eligibility_criteria: "",
        minimum_cgpa: "",
        application_start: "",
        application_deadline: ""
    }

}

function editDrive(drive) {

    showForm.value = true
    isEditing.value = true
    editingDriveId.value = drive.id

    form.value = { ...drive }

}

function cancelForm() {

    showForm.value = false
    isEditing.value = false
    editingDriveId.value = null

}

async function createDrive() {

    try {

        const payload = { ...form.value }

        payload.job_title = payload.job_title.trim()
        payload.job_description = payload.job_description.trim()
        payload.job_location = payload.job_location.trim()
        payload.job_type = payload.job_type.trim()
        payload.job_mode = payload.job_mode.trim()

        payload.salary_package = Number(payload.salary_package)

        if (payload.eligibility_criteria != null) {
            payload.eligibility_criteria = payload.eligibility_criteria.trim()
            if (payload.eligibility_criteria === "")
                delete payload.eligibility_criteria
        }

        if (payload.minimum_cgpa == null || payload.minimum_cgpa === "")
            delete payload.minimum_cgpa
        else
            payload.minimum_cgpa = Number(payload.minimum_cgpa)
        
        const response = await companyCreateDrive(payload)

        toast.action(response.message)

        cancelForm()

        await loadDrives()

    }

    catch (err) {

        toast.action(err.response?.data?.message || "Something went wrong.")

    }

}

async function updateDrive() {

    try {

        const payload = { ...form.value }

        payload.job_title = payload.job_title.trim()
        payload.job_description = payload.job_description.trim()
        payload.job_location = payload.job_location.trim()
        payload.job_type = payload.job_type.trim()
        payload.job_mode = payload.job_mode.trim()

        payload.salary_package = Number(payload.salary_package)

        if (payload.eligibility_criteria != null) {
            payload.eligibility_criteria = payload.eligibility_criteria.trim()
            if (payload.eligibility_criteria === "")
                delete payload.eligibility_criteria
        }

        if (payload.minimum_cgpa == null || payload.minimum_cgpa === "")
            delete payload.minimum_cgpa
        else
            payload.minimum_cgpa = Number(payload.minimum_cgpa)

        const response = await companyUpdateDrive(editingDriveId.value, payload)

        toast.action(response.message)

        cancelForm()

        await loadDrives()

    }

    catch (err) {

        toast.action(err.response?.data?.message || "Something went wrong.")

    }

}

async function saveDrive() {

    if (isEditing.value)
        await updateDrive()

    else
        await createDrive()

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
    router.push({name: "company-drive-application-list", params: {driveId: driveId}})
}

async function deleteDrive(driveId) {

    openConfirm("Are you sure you want to delete this drive?",
        async () => {
            try {
                const response = await companyDeleteDrive(driveId)
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
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold mb-0">Drives</h2>
            <button class="btn btn-primary d-inline-flex align-items-center gap-2" v-on:click="newDrive">
                <i class="bi bi-plus-circle me-1"></i><span>New Drive</span>
            </button>
        </div>
        <div v-if="showForm" class="card shadow-sm rounded-4 mb-4">
            <div class="card-body">
                <h4 class="fw-bold mb-4"> {{ isEditing ? "Update Drive" : "Create Drive" }} </h4>
                <form v-on:submit.prevent="saveDrive">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Job Title</label>
                            <input v-model="form.job_title" class="form-control" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Job Location</label>
                            <input v-model="form.job_location" class="form-control" required>
                        </div>
                        <div class="col-12">
                            <label class="form-label">Job Description</label>
                            <textarea rows="4" class="form-control" v-model="form.job_description" required></textarea>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Job Type</label>
                            <select class="form-select" v-model="form.job_type" required>
                                <option value="" disabled>Select</option>
                                <option>Permanent</option>
                                <option>Internship</option>
                                <option>Contract</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Job Mode</label>
                            <select class="form-select" v-model="form.job_mode" required>
                                <option value="" disabled>Select</option>
                                <option>Onsite</option>
                                <option>Hybrid</option>
                                <option>Remote</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Salary Package</label>
                            <input type="number" step="0.01" class="form-control" v-model="form.salary_package" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Minimum CGPA</label>
                            <input type="number" step="0.01" class="form-control" v-model="form.minimum_cgpa">
                        </div>
                        <div class="col-12">
                            <label class="form-label">Eligibility Criteria</label>
                            <textarea rows="4" class="form-control" v-model="form.eligibility_criteria"></textarea>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Application Start</label>
                            <input type="datetime-local" class="form-control" v-model="form.application_start" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Application Deadline</label>
                            <input type="datetime-local" class="form-control" v-model="form.application_deadline" required>
                        </div>
                    </div>
                    <div class="mt-4 d-flex gap-2">
                        <button type="submit" class="btn btn-success"> {{ isEditing ? "Update Drive" : "Create Drive" }} </button>
                        <button type="button" class="btn btn-secondary" v-on:click="cancelForm">Cancel</button>
                    </div>
                </form>
            </div>
        </div>
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
                        mode="company"
                        v-on:view="viewDrive"
                        v-on:edit="editDrive(drive)"
                        v-on:delete="deleteDrive"
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

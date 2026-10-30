<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"

import { useToastStore } from "../../stores/toast"

import ApplicationCard from "../../components/cards/ApplicationCard.vue"

import { getCompanyDriveApplications, companyUpdateApplication } from "../../services/company"

const router = useRouter()
const route = useRoute()

const toast = useToastStore()

const driveId = route.params.driveId

const applications = ref([])
const loading = ref(false)
const error = ref("")

const search = ref("")
const applicationStatusFilter = ref("")
const interviewStatusFilter = ref("")
const placementStatusFilter = ref("")

const showForm = ref(false)
const editingApplicationId = ref(null)

const hasInterview = ref(false)
const hasPlacement = ref(false)

const form = ref({
    application_status: "",
    interview_status: "",
    placement_status: "",
    interview_mode: "",
    interview_start_datetime: "",
    interview_end_datetime: "",
    joining_datetime: ""
})

const filteredApplications = computed(() => {

    return applications.value.filter(application => {

        const matchesSearch = application.student_name.toLowerCase().includes(search.value.toLowerCase()) || application.job_title.toLowerCase().includes(search.value.toLowerCase()) || application.company_name.toLowerCase().includes(search.value.toLowerCase())

        const matchesApplicationStatus = !applicationStatusFilter.value || application.application_status === applicationStatusFilter.value

        const matchesInterviewStatus = !interviewStatusFilter.value || application.interview_status === interviewStatusFilter.value

        const matchesPlacementStatus = !placementStatusFilter.value || application.placement_status === placementStatusFilter.value

        return (
            matchesSearch &&
            matchesApplicationStatus &&
            matchesInterviewStatus &&
            matchesPlacementStatus
        )

    })

})

const applicationStatusOptions = computed(() => {

    switch (form.value.application_status) {

        case "Applied":
            return ["Applied", "Shortlisted", "Rejected"]

        case "Shortlisted":
            return ["Shortlisted"]

        case "Rejected":
            return ["Rejected"]
    }

})

const interviewStatusOptions = computed(() => {

    switch (form.value.interview_status) {

        case "Scheduled":
            return ["Scheduled", "Selected", "Not Selected"]

        case "Selected":
            return ["Selected"]

        case "Not Selected":
            return ["Not Selected"]
    }

})

const placementStatusOptions = computed(() => {

    switch (form.value.placement_status) {

        case "Offered":
            return ["Offered", "Accepted", "Declined"]

        case "Accepted":
            return ["Accepted"]

        case "Declined":
            return ["Declined"]
    }

})

async function loadApplications() {

    loading.value = true
    error.value = ""

    try {
        applications.value = await getCompanyDriveApplications(driveId)
    }

    catch (err) {
        error.value = err.response?.data?.message || "Failed to load applications."
    }

    finally {
        loading.value = false
    }

}

function editApplication(application) {

    showForm.value = true
    editingApplicationId.value = application.id

    hasInterview.value = application.interview_exists
    hasPlacement.value = application.placement_exists

    form.value = {
        application_status: application.application_status,
        interview_status: hasInterview.value ? application.interview_status : "",
        placement_status: hasPlacement.value ? application.placement_status : "",
        interview_mode: hasInterview.value ? application.interview_mode : "",
        interview_start_datetime: hasInterview.value ? application.interview_start_datetime : "",
        interview_end_datetime: hasInterview.value ? application.interview_end_datetime : "",
        joining_datetime: hasPlacement.value ? application.joining_datetime : ""
    }

}

function cancelForm() {

    showForm.value = false
    editingApplicationId.value = null

    hasInterview.value = false
    hasPlacement.value = false

}

async function updateApplication() {

    try {

        const payload = { ...form.value }

        if (!payload.interview_status) {
            delete payload.interview_status
        }

        if (!payload.placement_status) {
            delete payload.placement_status
        }

        if (!payload.interview_mode) {
            delete payload.interview_mode
        }

        if (!payload.interview_start_datetime) {
            delete payload.interview_start_datetime
        }

        if (!payload.interview_end_datetime) {
            delete payload.interview_end_datetime
        }

        if (!payload.joining_datetime) {
            delete payload.joining_datetime
        }

        const response = await companyUpdateApplication(editingApplicationId.value, payload)

        toast.action(response.message)

        cancelForm()

        await loadApplications()

    }

    catch (err) {

        toast.action(err.response?.data?.message || "Something went wrong.")

    }

}

function viewApplication(applicationId) {
    router.push({name: "company-drive-application-detail", params: {driveId: driveId, applicationId: applicationId}})
}

onMounted(loadApplications)
</script>

<template>
    <div class="container py-4">
        <h2 class="fw-bold mb-4">Applications</h2>
        <div v-if="showForm" class="card shadow-sm rounded-4 mb-4">
            <div class="card-body">
                <h4 class="fw-bold mb-4">Update Application</h4>
                <form v-on:submit.prevent="updateApplication">
                    <div class="row g-3">
                        <div class="col-md-4">
                            <label class="form-label">Application Status</label>
                            <select class="form-select" v-model="form.application_status" required>
                                <option v-for="status in applicationStatusOptions" v-bind:key="status" v-bind:value="status"> {{ status }} </option>
                            </select>
                        </div>
                        <div class="col-md-4" v-if="hasInterview">
                            <label class="form-label">Interview Status</label>
                            <select class="form-select" v-model="form.interview_status">
                                <option v-for="status in interviewStatusOptions" v-bind:key="status" v-bind:value="status"> {{ status }} </option>
                            </select>
                        </div>
                        <div class="col-md-4" v-if="hasPlacement">
                            <label class="form-label">Placement Status</label>
                            <select class="form-select" v-model="form.placement_status">
                                <option v-for="status in placementStatusOptions" v-bind:key="status" v-bind:value="status"> {{ status }} </option>
                            </select>
                        </div>
                    </div>
                    <div class="row g-3 mt-1">
                        <div class="col-md-6" v-if="hasInterview || form.application_status === 'Shortlisted'">
                            <label class="form-label">Interview Start Date and Time</label>
                            <input type="datetime-local" class="form-control" v-model="form.interview_start_datetime" v-bind:disabled="hasInterview && form.interview_status !== 'Scheduled'">
                        </div>
                        <div class="col-md-6" v-if="hasInterview || form.application_status === 'Shortlisted'">
                            <label class="form-label">Interview End Date and Time</label>
                            <input type="datetime-local" class="form-control" v-model="form.interview_end_datetime" v-bind:disabled="hasInterview && form.interview_status !== 'Scheduled'">
                        </div>
                    </div>
                    <div class="row g-3 mt-1">
                        <div class="col-md-6" v-if="hasInterview || form.application_status === 'Shortlisted'">
                            <label class="form-label">Interview Mode</label>
                            <select class="form-select" v-model="form.interview_mode" v-bind:disabled="hasInterview && form.interview_status !== 'Scheduled'">
                                <option value="" disabled>Select</option>
                                <option>Virtual</option>
                                <option>On-Campus</option>
                                <option>Off-Campus</option>
                            </select>
                        </div>
                        <div class="col-md-6" v-if="hasPlacement || form.interview_status === 'Selected'">
                            <label class="form-label">Joining Date and Time</label>
                            <input type="datetime-local" class="form-control" v-model="form.joining_datetime" v-bind:disabled="hasPlacement && form.placement_status !== 'Offered'">
                        </div>
                    </div>
                    <div class="mt-4 d-flex gap-2">
                        <button type="submit" class="btn btn-success">Update Application</button>
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
                    <input v-model="search" type="text" class="form-control" placeholder="Search by Student or Drive or Company Name">
                </div>
                <div class="col-md-2">
                    <select v-model="applicationStatusFilter" class="form-select">
                        <option value="">Application Status</option>
                        <option>Applied</option>
                        <option>Shortlisted</option>
                        <option>Rejected</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <select v-model="interviewStatusFilter" class="form-select">
                        <option value="">Interview Status</option>
                        <option>-</option>
                        <option>Scheduled</option>
                        <option>Selected</option>
                        <option>Not Selected</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <select v-model="placementStatusFilter" class="form-select">
                        <option value="">Placement Status</option>
                        <option>-</option>
                        <option>Offered</option>
                        <option>Accepted</option>
                        <option>Declined</option>
                    </select>
                </div>
            </div>
            <div class="row g-4">
                <div class="col-lg-6" v-for="application in filteredApplications" v-bind:key="application.id">
                    <ApplicationCard
                        v-bind:application="application"
                        mode="company"
                        v-on:view="viewApplication"
                        v-on:edit="editApplication(application)"
                    />
                </div>
                <div v-if="filteredApplications.length === 0" class="text-center py-5 text-muted">No applications found.</div>
            </div>
        </div>
    </div>
</template>

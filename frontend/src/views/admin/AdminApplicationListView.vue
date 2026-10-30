<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"

import ApplicationCard from "../../components/cards/ApplicationCard.vue"

import { getAdminCompanyDriveApplications, getAdminStudentApplications } from "../../services/admin"

const router = useRouter()
const route = useRoute()

const companyId = route.params.companyId
const driveId = route.params.driveId
const studentId = route.params.studentId

const isDriveView = companyId && driveId
const isStudentView = studentId

const applications = ref([])
const loading = ref(false)
const error = ref("")

const search = ref("")
const applicationStatusFilter = ref("")
const interviewStatusFilter = ref("")
const placementStatusFilter = ref("")

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

async function loadApplications() {

    loading.value = true
    error.value = ""

    try {
        if (isDriveView) {
            applications.value = await getAdminCompanyDriveApplications(companyId, driveId)
        } else if (isStudentView) {
            applications.value = await getAdminStudentApplications(studentId)
        }
    }

    catch (err) {
        error.value = err.response?.data?.message || "Failed to load applications."
    }

    finally {
        loading.value = false
    }

}

function viewApplication(applicationId) {

    if (isDriveView) {
        router.push({name: "admin-company-drive-application-detail", params: {companyId: companyId, driveId: driveId, applicationId: applicationId}})
    } else if (isStudentView) {
        router.push({name: "admin-student-application-detail", params: {studentId: studentId, applicationId: applicationId}})
    }

}

onMounted(loadApplications)
</script>

<template>
    <div class="container py-4">
        <h2 class="fw-bold mb-4">Applications</h2>
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
                        mode="admin"
                        v-on:view="viewApplication"
                    />
                </div>
                <div v-if="filteredApplications.length === 0" class="text-center py-5 text-muted">No applications found.</div>
            </div>
        </div>
    </div>
</template>

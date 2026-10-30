<template>
    <div class="container py-4">
        <div class="mb-4">
            <h3 class="fw-semibold mb-1">Company Dashboard</h3>
        </div>
        <div class="card border-0 rounded-4 mx-5 bg-primary-subtle">
            <div class="card-body p-3">
                <div class="row g-3 mb-4">
                    <div class="col-lg-6">
                        <div class="card border-0 shadow-sm rounded-4">
                            <div class="card-body p-2 px-3">
                                <h5 class="fw-semibold mb-4"><i class="bi bi-grid-1x2-fill text-primary me-3"></i>Platform Overview</h5>
                                <div class="row text-center align-items-center">
                                    <div class="col-6 border-end">
                                        <i class="bi bi-briefcase-fill fs-2 text-primary"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.platform.total_drives }} </h6>
                                        <p class="text-muted mb-0">Total Drives</p>
                                    </div>
                                    <div class="col-6">
                                        <i class="bi bi-file-earmark-text-fill fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.platform.total_applications }} </h6>
                                        <p class="text-muted mb-0">Total Applications</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="card shadow-sm rounded-4 border-0">
                            <div class="card-body p-2 px-3">
                                <h5 class="fw-semibold mb-4"><i class="bi bi-briefcase-fill text-primary me-3"></i>Drive Approval Status</h5>
                                <div class="row text-center align-items-center">
                                    <div class="col-4 border-end">
                                        <i class="bi bi-clock-fill fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.drive_approval.pending }} </h6>
                                        <p class="text-muted mb-0">Pending</p>
                                    </div>
                                    <div class="col-4 border-end">
                                        <i class="bi bi-check-circle-fill fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.drive_approval.approved }} </h6>
                                        <p class="text-muted mb-0">Approved</p>
                                    </div>
                                    <div class="col-4">
                                        <i class="bi bi-x-circle-fill fs-2 text-danger"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.drive_approval.rejected }} </h6>
                                        <p class="text-muted mb-0">Rejected</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row g-3">
                    <div class="col-lg-6">
                        <div class="card shadow-sm rounded-4 border-0">
                            <div class="card-body p-2 px-3">
                                <h5 class="fw-semibold mb-4"><i class="bi bi-people text-primary me-3"></i>Placement Count</h5>
                                <div class="row text-center align-items-center">
                                    <div class="col-4 border-end">
                                        <i class="bi bi-person-fill-add fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.placement.count.shortlist }} </h6>
                                        <p class="text-muted mb-0">Shortlisted</p>
                                    </div>
                                    <div class="col-4 border-end">
                                        <i class="bi bi-person-fill-check fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.placement.count.select }} </h6>
                                        <p class="text-muted mb-0">Selected</p>
                                    </div>
                                    <div class="col-4">
                                        <i class="bi bi-person-bounding-box fs-2 text-primary"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.placement.count.accept }} </h6>
                                        <p class="text-muted mb-0">Accepted</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="card shadow-sm rounded-4 border-0">
                            <div class="card-body p-2 px-3">
                                <h5 class="fw-semibold mb-4"><i class="bi bi-bullseye text-primary me-3"></i>Placement Rate</h5>
                                <div class="row text-center align-items-center">
                                    <div class="col-4 border-end">
                                        <i class="bi bi-person-fill-add fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.placement.rate.shortlist }}% </h6>
                                        <p class="text-muted mb-0">Shortlist</p>
                                    </div>
                                    <div class="col-4 border-end">
                                        <i class="bi bi-person-fill-check fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.placement.rate.select }}% </h6>
                                        <p class="text-muted mb-0">Select</p>
                                    </div>
                                    <div class="col-4">
                                        <i class="bi bi-person-bounding-box fs-2 text-primary"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.placement.rate.accept }}% </h6>
                                        <p class="text-muted mb-0">Accept</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="card border-0 rounded-4 mx-5 mt-5">
            <div class="card shadow rounded-4">
                <div class="card-body p-4 text-center">
                    <i class="bi bi-briefcase-fill fs-1 text-primary mb-3"></i>
                    <h5 class="fw-semibold mb-3">Manage Drives</h5>
                    <RouterLink v-bind:to="{ name: 'company-drive-list' }" class="btn btn-primary px-4">View Drives</RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { getCompanyDashboard } from "../../services/company"

const dashboard = ref({
    platform: {
        total_drives: 0,
        total_applications: 0
    },
    drive_approval: {
        pending: 0,
        approved: 0,
        rejected: 0
    },
    placement: {
        count: {
            shortlist: 0,
            select: 0,
            accept: 0
        },
        rate: {
            shortlist: 0,
            select: 0,
            accept: 0
        }
    }
})

async function loadDashboard() {
    dashboard.value = await getCompanyDashboard()
}

onMounted(loadDashboard)
</script>

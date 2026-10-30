<template>
    <div class="container py-4">
        <div class="mb-4">
            <h3 class="fw-semibold mb-1">Student Dashboard</h3>
        </div>
        <div class="card border-0 rounded-4 mx-5 bg-primary-subtle">
            <div class="card-body p-3">
                <div class="row g-3 mb-4">
                    <div class="col-lg-4">
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
                                        <i class="bi bi-patch-check-fill fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.platform.eligible_drives }} </h6>
                                        <p class="text-muted mb-0">Eligible Drives</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4">
                        <div class="card shadow-sm rounded-4 border-0">
                            <div class="card-body p-2 px-3">
                                <h5 class="fw-semibold mb-4"><i class="bi bi-calendar3 text-primary me-3"></i>Drive Phase</h5>
                                <div class="row text-center align-items-center">
                                    <div class="col-4 border-end">
                                        <i class="bi bi-clock-fill fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.drive_phase.upcoming }} </h6>
                                        <p class="text-muted mb-0">Upcoming</p>
                                    </div>
                                    <div class="col-4 border-end">
                                        <i class="bi bi-play-circle-fill fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.drive_phase.ongoing }} </h6>
                                        <p class="text-muted mb-0">Ongoing</p>
                                    </div>
                                    <div class="col-4">
                                        <i class="bi bi-x-circle-fill fs-2 text-danger"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.drive_phase.closed }} </h6>
                                        <p class="text-muted mb-0">Closed</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4">
                        <div class="card shadow-sm rounded-4 border-0">
                            <div class="card-body p-2 px-3">
                                <h5 class="fw-semibold mb-4"><i class="bi bi-bullseye text-primary me-3"></i>Application Performance</h5>
                                <div class="row text-center align-items-center">
                                    <div class="col-4 border-end">
                                        <i class="bi bi-person-fill-add fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.application.performance.shortlist }}% </h6>
                                        <p class="text-muted mb-0">Shortlist</p>
                                    </div>
                                    <div class="col-4 border-end">
                                        <i class="bi bi-person-fill-check fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.application.performance.selection }}% </h6>
                                        <p class="text-muted mb-0">Selection</p>
                                    </div>
                                    <div class="col-4">
                                        <i class="bi bi-person-bounding-box fs-2 text-primary"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.application.performance.acceptance }}% </h6>
                                        <p class="text-muted mb-0">Acceptance</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row g-3">
                    <div class="col-lg-12">
                        <div class="card shadow-sm rounded-4 border-0">
                            <div class="card-body p-2 px-3">
                                <h5 class="fw-semibold mb-4"><i class="bi bi-diagram-3 text-primary me-3"></i>Application Stage</h5>
                                <div class="row text-center align-items-center">
                                    <div class="col border-end">
                                        <i class="bi bi-person-exclamation fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.application.stage.applied }} </h6>
                                        <p class="text-muted mb-0">Applied</p>
                                    </div>
                                    <div class="col border-end">
                                        <i class="bi bi-person-add fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.application.stage.shortlisted }} </h6>
                                        <p class="text-muted mb-0">Shortlisted</p>
                                    </div>
                                    <div class="col border-end">
                                        <i class="bi bi-person-x fs-2 text-danger"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.application.stage.rejected }} </h6>
                                        <p class="text-muted mb-0">Rejected</p>
                                    </div>
                                    <div class="col border-end">
                                        <i class="bi bi-person-gear fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.application.stage.scheduled }} </h6>
                                        <p class="text-muted mb-0">Scheduled</p>
                                    </div>
                                    <div class="col border-end">
                                        <i class="bi bi-person-check fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.application.stage.selected }} </h6>
                                        <p class="text-muted mb-0">Selected</p>
                                    </div>
                                    <div class="col border-end">
                                        <i class="bi bi-person-x fs-2 text-danger"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.application.stage.not_selected }} </h6>
                                        <p class="text-muted mb-0">Not Selected</p>
                                    </div>
                                    <div class="col border-end">
                                        <i class="bi bi-person-dash fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.application.stage.offered }} </h6>
                                        <p class="text-muted mb-0">Offered</p>
                                    </div>
                                    <div class="col border-end">
                                        <i class="bi bi-person-lock fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.application.stage.accepted }} </h6>
                                        <p class="text-muted mb-0">Accepted</p>
                                    </div>
                                    <div class="col">
                                        <i class="bi bi-person-slash fs-2 text-danger"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.application.stage.declined }} </h6>
                                        <p class="text-muted mb-0">Declined</p>
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
                    <i class="bi bi-buildings-fill fs-1 text-primary mb-3"></i>
                    <h5 class="fw-semibold mb-3">Explore Companies</h5>
                    <RouterLink v-bind:to="{ name: 'student-company-list' }" class="btn btn-primary px-4">View Companies</RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { getStudentDashboard } from "../../services/student"

const dashboard = ref({
    platform: {
        total_drives: 0,
        eligible_drives: 0
    },
    drive_phase: {
        upcoming: 0,
        ongoing: 0,
        closed: 0
    },
    application: {
        stage: {
            applied: 0,
            shortlisted: 0,
            rejected: 0,
            scheduled: 0,
            selected: 0,
            not_selected: 0,
            offered: 0,
            accepted: 0,
            declined: 0
        },
        performance: {
            shortlist: 0,
            selection: 0,
            acceptance: 0
        }
    }
})

async function loadDashboard() {
    dashboard.value = await getStudentDashboard()
}

onMounted(loadDashboard)
</script>

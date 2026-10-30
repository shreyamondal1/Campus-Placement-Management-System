<template>
    <div class="container py-4">
        <div class="mb-4">
            <h3 class="fw-semibold mb-1">Admin Dashboard</h3>
        </div>
        <div class="card border-0 rounded-4 mx-5 bg-primary-subtle">
            <div class="card-body p-3">
                <div class="row g-3 mb-4">
                    <div class="col-lg-12">
                        <div class="card border-0 shadow-sm rounded-4">
                            <div class="card-body p-2 px-3">
                                <h5 class="fw-semibold mb-4"><i class="bi bi-grid-1x2-fill text-primary me-3"></i>Platform Overview</h5>
                                <div class="row text-center align-items-center">
                                    <div class="col-3 border-end">
                                        <i class="bi bi-buildings-fill fs-2 text-primary"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.platform.total_companies }} </h6>
                                        <p class="text-muted mb-0">Total Companies</p>
                                    </div>
                                    <div class="col-3 border-end">
                                        <i class="bi bi-mortarboard-fill fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.platform.total_students }} </h6>
                                        <p class="text-muted mb-0">Total Students</p>
                                    </div>
                                    <div class="col-3 border-end">
                                        <i class="bi bi-briefcase-fill fs-2 text-danger"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.platform.total_drives }} </h6>
                                        <p class="text-muted mb-0">Total Drives</p>
                                    </div>
                                    <div class="col-3">
                                        <i class="bi bi-file-earmark-text-fill fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.platform.total_applications }} </h6>
                                        <p class="text-muted mb-0">Total Applications</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row g-3 mb-4">
                    <div class="col-lg-6">
                        <div class="card shadow-sm rounded-4 border-0">
                            <div class="card-body p-2 px-3">
                                <h5 class="fw-semibold mb-4"><i class="bi bi-buildings-fill text-primary me-3"></i>Company Approval Status</h5>
                                <div class="row text-center align-items-center">
                                    <div class="col-4 border-end">
                                        <i class="bi bi-clock-fill fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.approval.companies.pending }} </h6>
                                        <p class="text-muted mb-0">Pending</p>
                                    </div>
                                    <div class="col-4 border-end">
                                        <i class="bi bi-check-circle-fill fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.approval.companies.approved }} </h6>
                                        <p class="text-muted mb-0">Approved</p>
                                    </div>
                                    <div class="col-4">
                                        <i class="bi bi-x-circle-fill fs-2 text-danger"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.approval.companies.rejected }} </h6>
                                        <p class="text-muted mb-0">Rejected</p>
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
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.approval.drives.pending }} </h6>
                                        <p class="text-muted mb-0">Pending</p>
                                    </div>
                                    <div class="col-4 border-end">
                                        <i class="bi bi-check-circle-fill fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.approval.drives.approved }} </h6>
                                        <p class="text-muted mb-0">Approved</p>
                                    </div>
                                    <div class="col-4">
                                        <i class="bi bi-x-circle-fill fs-2 text-danger"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.approval.drives.rejected }} </h6>
                                        <p class="text-muted mb-0">Rejected</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row g-3 mb-4">
                    <div class="col-lg-6">
                        <div class="card shadow-sm rounded-4 border-0">
                            <div class="card-body p-2 px-3">
                                <h5 class="fw-semibold mb-4"><i class="bi bi-buildings-fill text-primary me-3"></i>Company User Status</h5>
                                <div class="row text-center align-items-center">
                                    <div class="col-4 border-end">
                                        <i class="bi bi-check-circle-fill fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.user.companies.active }} </h6>
                                        <p class="text-muted mb-0">Active</p>
                                    </div>
                                    <div class="col-4 border-end">
                                        <i class="bi bi-clock-fill fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.user.companies.disabled }} </h6>
                                        <p class="text-muted mb-0">Disabled</p>
                                    </div>
                                    <div class="col-4">
                                        <i class="bi bi-x-circle-fill fs-2 text-danger"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.user.companies.blacklisted }} </h6>
                                        <p class="text-muted mb-0">Blacklisted</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <div class="card shadow-sm rounded-4 border-0">
                            <div class="card-body p-2 px-3">
                                <h5 class="fw-semibold mb-4"><i class="bi bi-mortarboard-fill text-primary me-3"></i>Student User Status</h5>
                                <div class="row text-center align-items-center">
                                    <div class="col-4 border-end">
                                        <i class="bi bi-check-circle-fill fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.user.students.active }} </h6>
                                        <p class="text-muted mb-0">Active</p>
                                    </div>
                                    <div class="col-4 border-end">
                                        <i class="bi bi-clock-fill fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.user.students.disabled }} </h6>
                                        <p class="text-muted mb-0">Disabled</p>
                                    </div>
                                    <div class="col-4">
                                        <i class="bi bi-x-circle-fill fs-2 text-danger"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.user.students.blacklisted }} </h6>
                                        <p class="text-muted mb-0">Blacklisted</p>
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
                                <h5 class="fw-semibold mb-4"><i class="bi bi-currency-rupee text-primary me-3"></i>Placement Salary</h5>
                                <div class="row text-center align-items-center">
                                    <div class="col-4 border-end">
                                        <i class="bi bi-graph-up-arrow fs-2 text-primary"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.placement.salary.average }} LPA</h6>
                                        <p class="text-muted mb-0">Average</p>
                                    </div>
                                    <div class="col-4 border-end">
                                        <i class="bi bi-bar-chart-line-fill fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.placement.salary.median }} LPA</h6>
                                        <p class="text-muted mb-0">Median</p>
                                    </div>
                                    <div class="col-4">
                                        <i class="bi bi-trophy-fill fs-2 text-warning"></i>
                                        <h6 class="fw-semibold mt-1"> {{ dashboard.placement.salary.highest }} LPA</h6>
                                        <p class="text-muted mb-0">Highest</p>
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
                                        <h6 class="fw-semibold mt-1">{{ dashboard.placement.rate.shortlist }}%</h6>
                                        <p class="text-muted mb-0">Shortlist</p>
                                    </div>
                                    <div class="col-4 border-end">
                                        <i class="bi bi-person-fill-check fs-2 text-success"></i>
                                        <h6 class="fw-semibold mt-1">{{ dashboard.placement.rate.select }}%</h6>
                                        <p class="text-muted mb-0">Select</p>
                                    </div>
                                    <div class="col-4">
                                        <i class="bi bi-person-bounding-box fs-2 text-primary"></i>
                                        <h6 class="fw-semibold mt-1">{{ dashboard.placement.rate.accept }}%</h6>
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
            <div class="row g-3">
                <div class="col-lg-6">
                    <div class="card shadow rounded-4">
                        <div class="card-body p-4 text-center">
                            <i class="bi bi-buildings-fill fs-1 text-primary mb-3"></i>
                            <h5 class="fw-semibold mb-3">Manage Companies</h5>
                            <RouterLink v-bind:to="{ name: 'admin-company-list' }" class="btn btn-primary px-4">View Companies</RouterLink>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="card shadow rounded-4">
                        <div class="card-body p-4 text-center">
                            <i class="bi bi-mortarboard-fill fs-1 text-success mb-3"></i>
                            <h5 class="fw-semibold mb-3">Manage Students</h5>
                            <RouterLink v-bind:to="{ name: 'admin-student-list' }" class="btn btn-success px-4">View Students</RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { getAdminDashboard } from "../../services/admin"

const dashboard = ref({
    platform: {
        total_companies: 0,
        total_students: 0,
        total_drives: 0,
        total_applications: 0
    },
    approval: {
        companies: {
            pending: 0,
            approved: 0,
            rejected: 0
        },
        drives: {
            pending: 0,
            approved: 0,
            rejected: 0
        }
    },
    user: {
        companies: {
            active: 0,
            disabled: 0,
            blacklisted: 0
        },
        students: {
            active: 0,
            disabled: 0,
            blacklisted: 0
        }
    },
    placement: {
        salary: {
            average: 0,
            median: 0,
            highest: 0
        },
        rate: {
            shortlist: 0,
            select: 0,
            accept: 0
        }
    }
})

async function loadDashboard() {
    dashboard.value = await getAdminDashboard()
}

onMounted(loadDashboard)
</script>

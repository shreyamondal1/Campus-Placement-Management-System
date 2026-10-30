<script setup>
defineProps({
    drive: {
        type: Object,
        required: true
    },
    mode: {
        type: String,
        required: true
    }
})
</script>

<template>
    <div class="card shadow-sm">
        <div class="card-header bg-primary-subtle">
            <h5 class="mb-0"><i class="bi bi-briefcase-fill me-2"></i>Drive</h5>
        </div>
        <div class="card-body">
            <h6 class="fw-semibold mb-3">Summary</h6>
            <div class="row g-3 mb-4">
                <div class="col-md-6">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Designation</div>
                        <div class="fw-semibold mt-2"> {{ drive.job_title }} </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Location</div>
                        <div class="fw-semibold mt-2"> {{ drive.job_location }} </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Type</div>
                        <span class="fw-semibold mt-2"> {{ drive.job_type }} </span>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Mode</div>
                        <span class="fw-semibold mt-2"> {{ drive.job_mode }} </span>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Salary</div>
                        <div class="fw-semibold mt-2"> {{ (drive.salary_package / 100000).toFixed(2) }} LPA</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Minimum CGPA</div>
                        <div class="fw-semibold mt-2"> {{ drive.minimum_cgpa ?? "-" }} </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Drive Status</div>
                        <span class="badge mt-2" v-bind:class="{
                            'text-bg-warning': drive.drive_status === 'Upcoming',
                            'text-bg-success': drive.drive_status === 'Ongoing',
                            'text-bg-danger': drive.drive_status === 'Closed'
                        }"> {{ drive.drive_status }} </span>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="border rounded p-3 h-100">
                        <template v-if="mode === 'student'">
                            <div class="text-muted small">Eligibility Status</div>
                            <span class="badge mt-2" v-bind:class="{
                                'text-bg-success': drive.eligible_status === 'Eligible',
                                'text-bg-danger': drive.eligible_status === 'Not Eligible'
                            }"> {{ drive.eligible_status }} </span>
                        </template>
                        <template v-else>
                            <div class="text-muted small">Approval Status</div>
                            <span class="badge mt-2" v-bind:class="{
                                'text-bg-warning': drive.approval_status === 'Pending',
                                'text-bg-success': drive.approval_status === 'Approved',
                                'text-bg-danger': drive.approval_status === 'Rejected'
                            }"> {{ drive.approval_status }} </span>
                        </template>
                    </div>
                </div>
            </div>
            <hr>
            <h6 class="fw-semibold mb-3">Job Description</h6>
            <div class="border rounded p-3 h-100 bg-light mb-3"> {{ drive.job_description }} </div>
            <h6 class="fw-semibold mb-3">Eligibility Criteria</h6>
            <div class="border rounded p-3 h-100 bg-light mb-3"> {{ drive.eligibility_criteria ?? "-" }} </div>
        </div>
    </div>
</template>

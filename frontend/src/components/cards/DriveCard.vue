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

const emit = defineEmits([
    "view",
    "approve",
    "reject",
    "reapprove",
    "edit",
    "delete",
    "apply",
    "withdraw"
])
</script>

<template>
    <div class="card shadow-sm rounded-4 h-100" v-on:click="emit('view', drive.id)">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h5 class="fw-bold mb-1"> {{ drive.job_title }} </h5>
                    <p class="fw-semibold fs-6"> {{ drive.job_location }} </p>
                </div>
                <div class="text-end">                    
                    <template v-if="mode === 'student'">
                        <span class="badge d-block mb-2" v-bind:class="{
                            'text-bg-success': drive.eligible_status === 'Eligible',
                            'text-bg-danger': drive.eligible_status === 'Not Eligible'
                        }"> {{ drive.eligible_status }} </span>
                    </template>
                    <template v-else>
                        <span class="badge d-block mb-2" v-bind:class="{
                            'text-bg-warning': drive.approval_status === 'Pending',
                            'text-bg-success': drive.approval_status === 'Approved',
                            'text-bg-danger': drive.approval_status === 'Rejected'
                        }"> {{ drive.approval_status }} </span>
                    </template>
                    <span class="badge d-block" v-bind:class="{
                        'text-bg-warning': drive.drive_status === 'Upcoming',
                        'text-bg-success': drive.drive_status === 'Ongoing',
                        'text-bg-danger': drive.drive_status === 'Closed'
                    }"> {{ drive.drive_status }} </span>
                </div>
            </div>
            <div class="mb-1">
                <span class="badge border border-dark text-dark me-2"> {{ drive.job_type }} </span>
                <span class="badge border border-dark text-dark me-2"> {{ drive.job_mode }} </span>
                <span class="badge border border-dark text-dark me-2"> {{ (drive.salary_package / 100000).toFixed(2) }} LPA</span>
                <span class="badge border border-dark text-dark">Min. CGPA {{ drive.minimum_cgpa ?? "-" }} </span>
            </div>
            <template v-if="mode === 'admin'">
                <hr>
                <div class="d-flex justify-content-center gap-2">
                    <template v-if="drive.approval_status === 'Pending'">
                        <button class="btn btn-success btn-sm" v-on:click.stop="emit('approve', drive.id)">Approve</button>
                        <button class="btn btn-danger btn-sm" v-on:click.stop="emit('reject', drive.id)">Reject</button>
                    </template>
                    <template v-else-if="drive.approval_status === 'Rejected'">
                        <button class="btn btn-warning btn-sm" v-on:click.stop="emit('reapprove', drive.id)">Reapprove</button>
                    </template>
                </div>
            </template>
            <template v-else-if="mode === 'company'">
                <hr>
                <div class="d-flex justify-content-center gap-2">
                    <button class="btn btn-primary btn-sm" v-on:click.stop="emit('edit', drive.id)">Edit</button>
                    <button class="btn btn-danger btn-sm" v-on:click.stop="emit('delete', drive.id)">Delete</button>
                </div>
            </template>
            <template v-else-if="mode === 'student'">
                <hr>
                <div class="d-flex justify-content-center gap-2">
                    <template v-if="!drive.application_exists">
                        <button class="btn btn-success btn-sm" v-bind:disabled="drive.drive_status !== 'Ongoing' || drive.eligible_status !== 'Eligible'" v-on:click.stop="emit('apply', drive.id)">Apply</button>
                    </template>
                    <template v-else>
                        <button class="btn btn-danger btn-sm" v-bind:disabled="drive.drive_status !== 'Ongoing'" v-on:click.stop="emit('withdraw', drive.id)">Withdraw</button>
                    </template>
                </div>
            </template>
        </div>
    </div>
</template>

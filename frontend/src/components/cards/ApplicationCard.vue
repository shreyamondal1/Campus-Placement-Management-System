<script setup>
defineProps({
    application: {
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
    "edit"
])
</script>

<template>
    <div class="card shadow-sm rounded-4 h-100" v-on:click="emit('view', application.id)">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h5 class="fw-bold mb-1"> {{ application.student_name }} </h5>
                    <h6 class="fw-semibold mb-1"> {{ application.job_title }} </h6>
                    <p class="fw-medium"> {{ application.company_name }} </p>
                </div>
                <div class="text-end">
                    <span class="badge d-block mb-2" v-bind:class="{
                        'text-bg-warning': application.application_status === 'Applied',
                        'text-bg-success': application.application_status === 'Shortlisted',
                        'text-bg-danger': application.application_status === 'Rejected'
                    }"> {{ application.application_status }} </span>
                    <span class="badge d-block mb-2" v-bind:class="{
                        'text-bg-secondary': application.interview_status === '-',
                        'text-bg-warning': application.interview_status === 'Scheduled',
                        'text-bg-success': application.interview_status === 'Selected',
                        'text-bg-danger': application.interview_status === 'Not Selected'
                    }"> {{ application.interview_status }} </span>
                    <span class="badge d-block" v-bind:class="{
                        'text-bg-secondary': application.placement_status === '-',
                        'text-bg-warning': application.placement_status === 'Offered',
                        'text-bg-success': application.placement_status === 'Accepted',
                        'text-bg-danger': application.placement_status === 'Declined'
                    }"> {{ application.placement_status }} </span>
                </div>
            </div>
            <template v-if="mode === 'company'">
                <hr>
                <div class="d-flex justify-content-center gap-2">
                    <button class="btn btn-primary btn-sm" v-on:click.stop="emit('edit', application.id)">Edit</button>
                </div>
            </template>
        </div>
    </div>
</template>

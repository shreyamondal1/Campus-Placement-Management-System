<script setup>
import { computed } from "vue"

const props = defineProps({
    application: {
        type: Object,
        required: true
    },
    mode: {
        type: String,
        required: true
    }
})

const stages = computed(() => {

    const stagesToShow = []

    if (props.application.application_status === "-") {
        return stagesToShow
    }

    stagesToShow.push({
        label: "Applied",
        variant: "primary"
    })

    if (props.application.application_status === "Rejected") {
        stagesToShow.push({
            label: "Rejected",
            variant: "danger"
        })
        return stagesToShow
    }

    if (props.application.application_status === "Shortlisted") {
        stagesToShow.push({
            label: "Shortlisted",
            variant: "success"
        })
    }

    if (props.application.interview_status === "-") {
        stagesToShow[stagesToShow.length - 1].variant = "warning"
        return stagesToShow
    }      

    stagesToShow.push({
        label: "Scheduled",
        variant: "primary"
    })

    if (props.application.interview_status === "Not Selected") {
        stagesToShow.push({
            label: "Not Selected",
            variant: "danger"
        })
        return stagesToShow
    }

    if (props.application.interview_status === "Selected") {
        stagesToShow.push({
            label: "Selected",
            variant: "success"
        })
    }

    if (props.application.placement_status === "-") {
        stagesToShow[stagesToShow.length - 1].variant = "warning"
        return stagesToShow
    }

    stagesToShow.push({
        label: "Offered",
        variant: "primary"
    })

    if (props.application.placement_status === "Declined") {
        stagesToShow.push({
            label: "Declined",
            variant: "danger"
        })
        return stagesToShow
    }

    if (props.application.placement_status === "Accepted") {
        stagesToShow.push({
            label: "Accepted",
            variant: "success"
        })
    }

    const lastStage = stagesToShow[stagesToShow.length - 1]

    if (lastStage.label === "Applied" || lastStage.label === "Scheduled" || lastStage.label === "Offered") {
        lastStage.variant = "warning"
    }

    return stagesToShow

})
</script>

<template>
    <div class="card shadow-sm">
        <div class="card-header bg-primary-subtle">
            <h5 class="mb-0"><i class="bi bi-file-earmark-text-fill me-2"></i>Application</h5>
        </div>
        <div class="card-body">
            <h6 class="fw-semibold mb-3">Status</h6>
            <template v-if="stages.length">
                <div class="d-flex flex-wrap align-items-center justify-content-center mb-4">
                    <template v-for="(stage, index) in stages" v-bind:key="stage.label">
                        <span class="badge fs-6 fw-medium px-3 py-2" v-bind:class="'text-bg-' + stage.variant"> {{ stage.label }} </span>
                        <i v-if="index < stages.length - 1" class="bi bi-arrow-right mx-2 text-muted"></i>
                    </template>
                </div>
            </template>
            <template v-else>
                <div class="border rounded bg-light p-3 text-muted text-center align-items-center justify-content-center mb-4">No application exists.</div>
            </template>
            <hr>
            <h6 class="fw-semibold mb-3">Schedule</h6>
            <div class="row g-3 mb-3">
                <div class="col-md-4">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Interview Mode</div>
                        <div class="fw-semibold mt-2"> {{ application.interview_mode }} </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Interview Date and Time</div>
                        <div class="fw-semibold mt-2"> {{ application.interview_datetime }} </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Joining Date and Time</div>
                        <div class="fw-semibold mt-2"> {{ application.joining_datetime }} </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

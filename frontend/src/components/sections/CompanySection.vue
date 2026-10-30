<script setup>
defineProps({
    company: {
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
            <h5 class="mb-0"><i class="bi bi-buildings-fill me-2"></i>Company</h5>
        </div>
        <div class="card-body">
            <h6 class="fw-semibold mb-3">Summary</h6>
            <div class="row g-3 mb-4">
                <div class="col-md-6">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Name</div>
                        <div class="fw-semibold mt-2"> {{ company.name }} </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Email</div>
                        <div class="fw-semibold mt-2"> {{ company.email }} </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Website</div>
                        <div class="fw-semibold mt-2"><a v-bind:href="company.website" class="btn btn-outline-primary"><i class="bi bi-globe me-2"></i>Visit Website</a></div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Industry</div>
                        <div class="fw-semibold mt-2"> {{ company.industry ?? "-" }} </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Type</div>
                        <div class="fw-semibold mt-2"> {{ company.type ?? "-" }} </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Company Status</div>
                        <span class="badge mt-2" v-bind:class="{
                            'text-bg-success': company.user_status === 'Active',
                            'text-bg-warning': company.user_status === 'Disabled',
                            'text-bg-dark': company.user_status === 'Blacklisted'
                        }"> {{ company.user_status }} </span>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Approval Status</div>
                        <span class="badge mt-2" v-bind:class="{
                            'text-bg-warning': company.approval_status === 'Pending',
                            'text-bg-success': company.approval_status === 'Approved',
                            'text-bg-danger': company.approval_status === 'Rejected'
                        }"> {{ company.approval_status }} </span>
                    </div>
                </div>
            </div>
            <hr>
            <h6 class="fw-semibold mb-3">Contact</h6>
            <div class="row g-3 mb-4">
                <div class="col-md-6">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">HR Name</div>
                        <div class="fw-semibold mt-2"> {{ company.hr_contact_name }} </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">HR Number</div>
                        <div class="fw-semibold mt-2"> {{ company.hr_contact_number }} </div>
                    </div>
                </div>
            </div>
            <hr>
            <h6 class="fw-semibold mb-3">About</h6>
            <div class="border rounded p-3 h-100 bg-light mb-3"> {{ company.description ?? "-" }} </div>
        </div>
    </div>
</template>

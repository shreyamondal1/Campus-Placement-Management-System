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

const emit = defineEmits([
    "view",
    "approve",
    "reject",
    "reapprove",
    "disable",
    "enable",
    "blacklist",
    "whitelist",
    "delete"
])
</script>

<template>
    <div class="card shadow-sm rounded-4 h-100" v-on:click="emit('view', company.id)">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <div class="d-flex align-items-center gap-2 mb-2">
                        <h5 class="fw-bold mb-1"> {{ company.name }} </h5>
                        <small><a v-bind:href="company.website" v-on:click.stop><i class="bi bi-globe"></i></a></small>
                    </div>
                    <div class="small mb-3">
                        <div class="text-muted"><i class="bi bi-person-fill me-1"></i> {{ company.username }} </div>
                        <div><a v-bind:href="`mailto:${company.email}`" class="text-decoration-none text-muted" v-on:click.stop><i class="bi bi-envelope-fill me-1"></i> {{ company.email }} </a></div>
                    </div>
                </div>
                <div class="text-end">
                    <template v-if="mode !== 'student'">
                        <span class="badge d-block mb-2" v-bind:class="{
                            'text-bg-warning': company.approval_status === 'Pending',
                            'text-bg-success': company.approval_status === 'Approved',
                            'text-bg-danger': company.approval_status === 'Rejected'
                        }"> {{ company.approval_status }} </span>
                        <span class="badge d-block" v-bind:class="{
                            'text-bg-success': company.user_status === 'Active',
                            'text-bg-warning': company.user_status === 'Disabled',
                            'text-bg-dark': company.user_status === 'Blacklisted'
                        }"> {{ company.user_status }} </span>
                    </template>
                </div>
            </div>
            <div class="mb-2">
                <span class="badge border border-dark text-dark me-2"> {{ company.type }} </span>
                <span class="badge border border-dark text-dark mb-3"> {{ company.industry }} </span>
                <p class="mb-3"> {{ company.description }} </p>
            </div>
            <template v-if="mode === 'admin'">
                <hr>
                <div class="d-flex justify-content-center gap-2 mb-3">
                    <template v-if="company.approval_status === 'Pending'">
                        <button class="btn btn-success btn-sm" v-on:click.stop="emit('approve', company.id)">Approve</button>
                        <button class="btn btn-danger btn-sm" v-on:click.stop="emit('reject', company.id)">Reject</button>
                    </template>
                    <template v-else-if="company.approval_status === 'Rejected'">
                        <button class="btn btn-warning btn-sm" v-on:click.stop="emit('reapprove', company.id)">Reapprove</button>
                    </template>
                </div>
                <div class="d-flex justify-content-center gap-2">
                    <template v-if="company.user_status === 'Active'">
                        <button class="btn btn-outline-warning btn-sm" v-on:click.stop="emit('disable', company.id)">Disable</button>
                        <button class="btn btn-outline-dark btn-sm" v-on:click.stop="emit('blacklist', company.id)">Blacklist</button>
                    </template>
                    <template v-else-if="company.user_status === 'Disabled'">
                        <button class="btn btn-outline-primary btn-sm" v-on:click.stop="emit('enable', company.id)">Enable</button>
                    </template>
                    <template v-else-if="company.user_status === 'Blacklisted'">
                        <button class="btn btn-outline-primary btn-sm" v-on:click.stop="emit('whitelist', company.id)">Whitelist</button>
                    </template>
                    <button class="btn btn-outline-danger btn-sm" v-on:click.stop="emit('delete', company.id)">Delete</button>
                </div>
            </template>
        </div>
    </div>
</template>

<script setup>
defineProps({
    student: {
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
    "disable",
    "enable",
    "blacklist",
    "whitelist",
    "delete"
])
</script>

<template>
    <div class="card shadow-sm rounded-4 h-100" v-on:click="emit('view', student.id)">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <div class="d-flex align-items-center gap-2 mb-2">
                        <h5 class="fw-bold mb-1"> {{ student.name }} </h5>
                        <small><a v-bind:href="student.linkedin" v-on:click.stop><i class="bi bi-linkedin me-1"></i></a></small>
                        <small><a v-bind:href="student.github" v-on:click.stop><i class="bi bi-github me-1"></i></a></small>
                        <small><a v-bind:href="student.portfolio" v-on:click.stop><i class="bi bi-person-vcard me-1"></i></a></small>
                        <small><a v-bind:href="student.resume" v-on:click.stop><i class="bi bi-file-earmark-pdf"></i></a></small>
                    </div>
                    <div class="small mb-3">
                        <div class="text-muted"><i class="bi bi-person-fill me-1"></i> {{ student.username }} </div>
                        <div><a v-bind:href="`mailto:${student.email}`" class="text-decoration-none text-muted" v-on:click.stop><i class="bi bi-envelope-fill me-1"></i> {{ student.email }} </a></div>
                    </div>
                </div>
                <div class="text-end">
                    <template v-if="mode !== 'company'">
                        <span class="badge d-block mb-4" v-bind:class="{
                            'text-bg-success': student.user_status === 'Active',
                            'text-bg-warning': student.user_status === 'Disabled',
                            'text-bg-dark': student.user_status === 'Blacklisted'
                        }"> {{ student.user_status }} </span>
                    </template>
                </div>
            </div>
            <div class="mb-2">
                <span class="badge border border-dark text-dark me-2"> {{ student.degree }} </span>
                <span class="badge border border-dark text-dark me-2"> {{ student.department }} </span>
                <span class="badge border border-dark text-dark me-2"> {{ student.graduation_year }} </span>
                <span class="badge border border-dark text-dark mb-1">CGPA: {{ student.cgpa }} </span>
            </div>
            <template v-if="mode === 'admin'">
                <hr>
                <div class="d-flex justify-content-center gap-2">
                    <template v-if="student.user_status === 'Active'">
                        <button class="btn btn-outline-warning btn-sm" v-on:click.stop="emit('disable', student.id)">Disable</button>
                        <button class="btn btn-outline-dark btn-sm" v-on:click.stop="emit('blacklist', student.id)">Blacklist</button>
                    </template>
                    <template v-else-if="student.user_status === 'Disabled'">
                        <button class="btn btn-outline-primary btn-sm" v-on:click.stop="emit('enable', student.id)">Enable</button>
                    </template>
                    <template v-else-if="student.user_status === 'Blacklisted'">
                        <button class="btn btn-outline-primary btn-sm" v-on:click.stop="emit('whitelist', student.id)">Whitelist</button>
                    </template>
                    <button class="btn btn-outline-danger btn-sm" v-on:click.stop="emit('delete', student.id)">Delete</button>
                </div>
            </template>
        </div>
    </div>
</template>

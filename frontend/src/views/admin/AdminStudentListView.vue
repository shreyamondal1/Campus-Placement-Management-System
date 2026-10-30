<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"

import { useToastStore } from "../../stores/toast"

import StudentCard from "../../components/cards/StudentCard.vue"

import { getAdminStudents, adminDisableStudent, adminEnableStudent, adminBlacklistStudent, adminWhitelistStudent, adminDeleteStudent } from "../../services/admin"

const router = useRouter()

const toast = useToastStore()

const students = ref([])
const loading = ref(false)
const error = ref("")

const search = ref("")
const userStatusFilter = ref("")

const filteredStudents = computed(() => {

    return students.value.filter(student => {

        const matchesSearch = student.name.toLowerCase().includes(search.value.toLowerCase())

        const matchesUserStatus = !userStatusFilter.value || student.user_status === userStatusFilter.value

        return (
            matchesSearch &&
            matchesUserStatus
        )

    })

})

const showConfirm = ref(false)
const confirmMessage = ref("")
const pendingAction = ref(null)

async function loadStudents() {

    loading.value = true
    error.value = ""

    try {
        students.value = await getAdminStudents()
    }

    catch (err) {
        error.value = err.response?.data?.message || "Failed to load students."
    }

    finally {
        loading.value = false
    }

}

function openConfirm(message, action) {

    showConfirm.value = true
    confirmMessage.value = message
    pendingAction.value = action

}

async function confirmAction() {

    showConfirm.value = false

    if (pendingAction.value) {
        await pendingAction.value()
        pendingAction.value = null
    }

}

function cancelAction() {

    showConfirm.value = false
    pendingAction.value = null

}

function viewStudent(studentId) {
    router.push({name: "admin-student-application-list", params: {studentId: studentId}})
}

async function disableStudent(studentId) {

    openConfirm("Are you sure you want to disable this student?",
        async () => {
            try {
                const response = await adminDisableStudent(studentId)
                toast.action(response.message)
                await loadStudents()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function enableStudent(studentId) {

    openConfirm("Are you sure you want to enable this student?",
        async () => {
            try {
                const response = await adminEnableStudent(studentId)
                toast.action(response.message)
                await loadStudents()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function blacklistStudent(studentId) {

    openConfirm("Are you sure you want to blacklist this student?",
        async () => {
            try {
                const response = await adminBlacklistStudent(studentId)
                toast.action(response.message)
                await loadStudents()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function whitelistStudent(studentId) {

    openConfirm("Are you sure you want to whitelist this student?",
        async () => {
            try {
                const response = await adminWhitelistStudent(studentId)
                toast.action(response.message)
                await loadStudents()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function deleteStudent(studentId) {

    openConfirm("Are you sure you want to delete this student?",
        async () => {
            try {
                const response = await adminDeleteStudent(studentId)
                toast.action(response.message)
                await loadStudents()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

onMounted(loadStudents)
</script>

<template>
    <div class="container py-4">
        <h2 class="fw-bold mb-4">Students</h2>
        <div v-if="loading" class="text-center py-5"><div class="spinner-border"></div></div>
        <div v-else-if="error" class="alert alert-danger"> {{ error }} </div>
        <div v-else>
            <div class="row mb-4">
                <div class="col-md-8">
                    <input v-model="search" type="text" class="form-control" placeholder="Search by Student Name">
                </div>
                <div class="col-md-4">
                    <select v-model="userStatusFilter" class="form-select">
                        <option value="">User Status</option>
                        <option>Active</option>
                        <option>Disabled</option>
                        <option>Blacklisted</option>
                    </select>
                </div>
            </div>
            <div class="row g-4">
                <div class="col-lg-6" v-for="student in filteredStudents" v-bind:key="student.id">
                    <StudentCard
                        v-bind:student="student"
                        mode="admin"
                        v-on:view="viewStudent"
                        v-on:disable="disableStudent"
                        v-on:enable="enableStudent"
                        v-on:blacklist="blacklistStudent"
                        v-on:whitelist="whitelistStudent"
                        v-on:delete="deleteStudent"
                    />
                </div>
                <div v-if="filteredStudents.length === 0" class="text-center py-5 text-muted">No students found.</div>
            </div>
            <div v-if="showConfirm" class="modal fade show" style="display:block; background-color:rgba(0,0,0,.5);">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Confirm Action</h5>
                        </div>
                        <div class="modal-body"> {{ confirmMessage }} </div>
                        <div class="modal-footer">
                            <button class="btn btn-success" v-on:click="cancelAction">Cancel</button>
                            <button class="btn btn-danger" v-on:click="confirmAction">Confirm</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

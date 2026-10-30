<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"

import { useToastStore } from "../../stores/toast"

import CompanyCard from "../../components/cards/CompanyCard.vue"

import { getAdminCompanies, adminApproveCompany, adminRejectCompany, adminReapproveCompany, adminDisableCompany, adminEnableCompany, adminBlacklistCompany, adminWhitelistCompany, adminDeleteCompany } from "../../services/admin"

const router = useRouter()

const toast = useToastStore()

const companies = ref([])
const loading = ref(false)
const error = ref("")

const search = ref("")
const approvalStatusFilter = ref("")
const userStatusFilter = ref("")

const filteredCompanies = computed(() => {

    return companies.value.filter(company => {

        const matchesSearch = company.name.toLowerCase().includes(search.value.toLowerCase())

        const matchesApprovalStatus = !approvalStatusFilter.value || company.approval_status === approvalStatusFilter.value

        const matchesUserStatus = !userStatusFilter.value || company.user_status === userStatusFilter.value

        return (
            matchesSearch &&
            matchesApprovalStatus &&
            matchesUserStatus
        )

    })

})

const showConfirm = ref(false)
const confirmMessage = ref("")
const pendingAction = ref(null)

async function loadCompanies() {

    loading.value = true
    error.value = ""

    try {
        companies.value = await getAdminCompanies()
    }

    catch (err) {
        error.value = err.response?.data?.message || "Failed to load companies."
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

function viewCompany(companyId) {
    router.push({name: "admin-company-drive-list", params: {companyId: companyId}})
}

async function approveCompany(companyId) {

    openConfirm("Are you sure you want to approve this company?",
        async () => {
            try {
                const response = await adminApproveCompany(companyId)
                toast.action(response.message)
                await loadCompanies()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function rejectCompany(companyId) {

    openConfirm("Are you sure you want to reject this company?",
        async () => {
            try {
                const response = await adminRejectCompany(companyId)
                toast.action(response.message)
                await loadCompanies()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function reapproveCompany(companyId) {

    openConfirm("Are you sure you want to reapprove this company?",
        async () => {
            try {
                const response = await adminReapproveCompany(companyId)
                toast.action(response.message)
                await loadCompanies()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function disableCompany(companyId) {

    openConfirm("Are you sure you want to disable this company?",
        async () => {
            try {
                const response = await adminDisableCompany(companyId)
                toast.action(response.message)
                await loadCompanies()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function enableCompany(companyId) {

    openConfirm("Are you sure you want to enable this company?",
        async () => {
            try {
                const response = await adminEnableCompany(companyId)
                toast.action(response.message)
                await loadCompanies()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function blacklistCompany(companyId) {

    openConfirm("Are you sure you want to blacklist this company?",
        async () => {
            try {
                const response = await adminBlacklistCompany(companyId)
                toast.action(response.message)
                await loadCompanies()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function whitelistCompany(companyId) {

    openConfirm("Are you sure you want to whitelist this company?",
        async () => {
            try {
                const response = await adminWhitelistCompany(companyId)
                toast.action(response.message)
                await loadCompanies()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

async function deleteCompany(companyId) {

    openConfirm("Are you sure you want to delete this company?",
        async () => {
            try {
                const response = await adminDeleteCompany(companyId)
                toast.action(response.message)
                await loadCompanies()
            } catch (err) {
                toast.action(err.response?.data?.message || "Something went wrong.")
            }
        }
    )

}

onMounted(loadCompanies)
</script>

<template>
    <div class="container py-4">
        <h2 class="fw-bold mb-4">Companies</h2>
        <div v-if="loading" class="text-center py-5"><div class="spinner-border"></div></div>
        <div v-else-if="error" class="alert alert-danger"> {{ error }} </div>
        <div v-else>
            <div class="row mb-4">
                <div class="col-md-6">
                    <input v-model="search" type="text" class="form-control" placeholder="Search by Company Name">
                </div>
                <div class="col-md-3">
                    <select v-model="approvalStatusFilter" class="form-select">
                        <option value="">Approval Status</option>
                        <option>Pending</option>
                        <option>Approved</option>
                        <option>Rejected</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <select v-model="userStatusFilter" class="form-select">
                        <option value="">User Status</option>
                        <option>Active</option>
                        <option>Disabled</option>
                        <option>Blacklisted</option>
                    </select>
                </div>
            </div>
            <div class="row g-4">
                <div class="col-lg-6" v-for="company in filteredCompanies" v-bind:key="company.id">
                    <CompanyCard
                        v-bind:company="company"
                        mode="admin"
                        v-on:view="viewCompany"
                        v-on:approve="approveCompany"
                        v-on:reject="rejectCompany"
                        v-on:reapprove="reapproveCompany"
                        v-on:disable="disableCompany"
                        v-on:enable="enableCompany"
                        v-on:blacklist="blacklistCompany"
                        v-on:whitelist="whitelistCompany"
                        v-on:delete="deleteCompany"
                    />
                </div>
                <div v-if="filteredCompanies.length === 0" class="text-center py-5 text-muted">No companies found.</div>
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

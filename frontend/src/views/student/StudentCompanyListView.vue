<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"

import CompanyCard from "../../components/cards/CompanyCard.vue"

import { getStudentCompanies } from "../../services/student"

const router = useRouter()

const companies = ref([])
const loading = ref(false)
const error = ref("")

const search = ref("")

const filteredCompanies = computed(() => {

    return companies.value.filter(company => {

        const matchesSearch = company.name.toLowerCase().includes(search.value.toLowerCase())

        return matchesSearch
    
    })

})

async function loadCompanies() {

    loading.value = true
    error.value = ""

    try {
        companies.value = await getStudentCompanies()
    }

    catch (err) {
        error.value = err.response?.data?.message || "Failed to load companies."
    }

    finally {
        loading.value = false
    }

}

function viewCompany(companyId) {
    router.push({name: "student-company-drive-list", params: {companyId: companyId}})
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
                <div class="col-md-12">
                    <input v-model="search" type="text" class="form-control" placeholder="Search by Company Name">
                </div>
            </div>
            <div class="row g-4">
                <div class="col-lg-6" v-for="company in filteredCompanies" v-bind:key="company.id">
                    <CompanyCard
                        v-bind:company="company"
                        mode="student"
                        v-on:view="viewCompany"
                    />
                </div>
                <div v-if="filteredCompanies.length === 0" class="text-center py-5 text-muted">No companies found.</div>
            </div>
        </div>
    </div>
</template>

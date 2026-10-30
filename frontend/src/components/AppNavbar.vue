<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"

import { useAuthStore } from "../stores/auth"

const router = useRouter()
const authStore = useAuthStore()

const navigation = {

    guest: [
        {
            label: "Home",
            route: "home"
        },
        {
            label: "Admin",
            children: [
                {
                    label: "Login",
                    route: "admin-login"
                }
            ]
        },
        {
            label: "Company",
            children: [
                {
                    label: "Register",
                    route: "company-register"
                },
                {
                    label: "Login",
                    route: "company-login"
                }
            ]
        },
        {
            label: "Student",
            children: [
                {
                    label: "Register",
                    route: "student-register"
                },
                {
                    label: "Login",
                    route: "student-login"
                }
            ]
        }
    ],

    admin: [
        {
            label: "Dashboard",
            route: "admin-dashboard"
        },
        {
            label: "Company",
            children: [
                {
                    label: "Browse Companies",
                    route: "admin-company-list"
                }
            ]
        },
        {
            label: "Student",
            children: [
                {
                    label: "Browse Students",
                    route: "admin-student-list"
                }
            ]
        }
    ],

    company: [
        {
            label: "Dashboard",
            route: "company-dashboard"
        },
        {
            label: "Drive",
            children: [
                {
                    label: "Browse Drives",
                    route: "company-drive-list"
                }
            ]
        }
    ],

    student: [
        {
            label: "Dashboard",
            route: "student-dashboard"
        },
        {
            label: "Company",
            children: [
                {
                    label: "Browse Companies",
                    route: "student-company-list"
                }
            ]
        }
    ]
}

const currentNavigation = computed(() => {

    if (!authStore.isLoggedIn) {
        return navigation.guest
    }

    switch (authStore.user.role) {

        case "Admin":
            return navigation.admin
        
        case "Company":
            return navigation.company
        
        case "Student":
            return navigation.student
        
        default:
            return navigation.guest
    }
})

async function logout() {

    await authStore.logout()

    await router.push({name: "home"})
}
</script>

<template>
    <nav class="app-navbar">
        <div class="container h-100 d-flex justify-content-center align-items-center">
            <ul class="navbar-nav flex-row">
                <li v-for="item in currentNavigation" v-bind:key="item.label" v-bind:class="['nav-item', 'me-3', item.children ? 'dropdown' : '']">
                    <RouterLink v-if="!item.children" v-bind:to="{ name: item.route }" class="nav-link fw-medium"> {{ item.label }} </RouterLink>
                    <template v-else>
                        <button class="nav-link fw-medium dropdown-toggle bg-transparent border-0" type="button" data-bs-toggle="dropdown"> {{ item.label }} </button>
                        <ul class="dropdown-menu">
                            <li v-for="child in item.children" v-bind:key="child.label">
                                <RouterLink class="dropdown-item" v-bind:to="{ name: child.route }"> {{ child.label }} </RouterLink>
                            </li>
                        </ul>
                    </template>
                </li>
            </ul>
            <div v-if="authStore.isLoggedIn" class="d-flex align-items-center ms-auto">
                <small><div class="fw-lighter text-white">You are logged in as</div></small>
                <span class="badge me-3 px-3 py-2">
                    <div class="fs-6 fw-medium mb-2"> {{ authStore.user.username }} </div>
                    <div class="fw-normal mt-2"><i class="bi bi-person-circle me-1"></i> {{ authStore.user.role }} </div>
                </span>
                <div class="dropdown">
                    <button class="btn btn-link fs-3 nav-menu p-0" data-bs-toggle="dropdown">
                        <i class="bi bi-list"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li>
                            <RouterLink class="dropdown-item" v-bind:to="{ name: `${authStore.user.role.toLowerCase()}-profile` }">View Account</RouterLink>
                        </li>
                        <li>
                            <RouterLink class="dropdown-item" v-bind:to="{ name: `${authStore.user.role.toLowerCase()}-inbox` }">Notifications</RouterLink>
                        </li>
                        <li>
                            <hr class="dropdown-divider">
                        </li>
                        <li>
                            <button class="dropdown-item" v-on:click="logout">Logout</button>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </nav>
</template>

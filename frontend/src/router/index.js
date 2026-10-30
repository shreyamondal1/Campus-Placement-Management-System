import { createRouter, createWebHistory } from "vue-router"

import { useAuthStore } from "../stores/auth"

import HomeView from "../views/HomeView.vue"

import AdminView from "../views/admin/AdminView.vue"
import CompanyView from "../views/company/CompanyView.vue"
import StudentView from "../views/student/StudentView.vue"

import RegisterView from "../views/auth/RegisterView.vue"
import LoginView from "../views/auth/LoginView.vue"

import AdminDashboardView from "../views/admin/AdminDashboardView.vue"
import CompanyDashboardView from "../views/company/CompanyDashboardView.vue"
import StudentDashboardView from "../views/student/StudentDashboardView.vue"

import AdminProfileView from "../views/admin/AdminProfileView.vue"
import CompanyProfileView from "../views/company/CompanyProfileView.vue"
import StudentProfileView from "../views/student/StudentProfileView.vue"

import AdminInboxView from "../views/admin/AdminInboxView.vue"
import CompanyInboxView from "../views/company/CompanyInboxView.vue"
import StudentInboxView from "../views/student/StudentInboxView.vue"

import AdminCompanyListView from "../views/admin/AdminCompanyListView.vue"
import AdminStudentListView from "../views/admin/AdminStudentListView.vue"
import AdminDriveListView from "../views/admin/AdminDriveListView.vue"
import AdminApplicationListView from "../views/admin/AdminApplicationListView.vue"
import AdminApplicationDetailView from "../views/admin/AdminApplicationDetailView.vue"

import CompanyDriveListView from "../views/company/CompanyDriveListView.vue"
import CompanyApplicationListView from "../views/company/CompanyApplicationListView.vue"
import CompanyApplicationDetailView from "../views/company/CompanyApplicationDetailView.vue"

import StudentCompanyListView from "../views/student/StudentCompanyListView.vue"
import StudentDriveListView from "../views/student/StudentDriveListView.vue"
import StudentDriveDetailView from "../views/student/StudentDriveDetailView.vue"

const routes = [
    {
        path: "/",
        name: "home",
        component: HomeView,
        meta: {
            guestOnly: true
        }
    },
    {
        path: "/admin",
        name: "admin",
        component: AdminView,
        meta: {
            guestOnly: true
        }
    },
    {
        path: "/company",
        name: "company",
        component: CompanyView,
        meta: {
            guestOnly: true
        }
    },
    {
        path: "/student",
        name: "student",
        component: StudentView,
        meta: {
            guestOnly: true
        }
    },
    {
        path: "/admin/login",
        name: "admin-login",
        component: LoginView,
        meta: {
            guestOnly: true,
            loginRole: "Admin"
        }
    },
    {
        path: "/company/register",
        name: "company-register",
        component: RegisterView,
        meta: {
            guestOnly: true,
            registrationRole: "Company"
        }
    },
    {
        path: "/company/login",
        name: "company-login",
        component: LoginView,
        meta: {
            guestOnly: true,
            loginRole: "Company"
        }
    },
    {
        path: "/student/register",
        name: "student-register",
        component: RegisterView,
        meta: {
            guestOnly: true,
            registrationRole: "Student"
        }
    },
    {
        path: "/student/login",
        name: "student-login",
        component: LoginView,
        meta: {
            guestOnly: true,
            loginRole: "Student"
        }
    },
    {
        path: "/admin/dashboard",
        name: "admin-dashboard",
        component: AdminDashboardView,
        meta: {
            requiresAuth: true,
            requiredRole: "Admin"
        }
    },
    {
        path: "/company/dashboard",
        name: "company-dashboard",
        component: CompanyDashboardView,
        meta: {
            requiresAuth: true,
            requiredRole: "Company"
        }
    },
    {
        path: "/student/dashboard",
        name: "student-dashboard",
        component: StudentDashboardView,
        meta: {
            requiresAuth: true,
            requiredRole: "Student"
        }
    },
    {
        path: "/admin/profile",
        name: "admin-profile",
        component: AdminProfileView,
        meta: {
            requiresAuth: true,
            requiredRole: "Admin"
        }
    },
    {
        path: "/company/profile",
        name: "company-profile",
        component: CompanyProfileView,
        meta: {
            requiresAuth: true,
            requiredRole: "Company"
        }
    },
    {
        path: "/student/profile",
        name: "student-profile",
        component: StudentProfileView,
        meta: {
            requiresAuth: true,
            requiredRole: "Student"
        }
    },
    {
        path: "/admin/inbox",
        name: "admin-inbox",
        component: AdminInboxView,
        meta: {
            requiresAuth: true,
            requiredRole: "Admin"
        }
    },
    {
        path: "/company/inbox",
        name: "company-inbox",
        component: CompanyInboxView,
        meta: {
            requiresAuth: true,
            requiredRole: "Company"
        }
    },
    {
        path: "/student/inbox",
        name: "student-inbox",
        component: StudentInboxView,
        meta: {
            requiresAuth: true,
            requiredRole: "Student"
        }
    },
    {
        path: "/admin/companies",
        name: "admin-company-list",
        component: AdminCompanyListView,
        meta: {
            requiresAuth: true,
            requiredRole: "Admin"
        }
    },
    {
        path: "/admin/companies/:companyId",
        name: "admin-company-drive-list",
        component: AdminDriveListView,
        meta: {
            requiresAuth: true,
            requiredRole: "Admin"
        }
    },
    {
        path: "/admin/companies/:companyId/:driveId",
        name: "admin-company-drive-application-list",
        component: AdminApplicationListView,
        meta: {
            requiresAuth: true,
            requiredRole: "Admin"
        }
    },
    {
        path: "/admin/companies/:companyId/:driveId/:applicationId",
        name: "admin-company-drive-application-detail",
        component: AdminApplicationDetailView,
        meta: {
            requiresAuth: true,
            requiredRole: "Admin"
        }
    },
    {
        path: "/admin/students",
        name: "admin-student-list",
        component: AdminStudentListView,
        meta: {
            requiresAuth: true,
            requiredRole: "Admin"
        }
    },
    {
        path: "/admin/students/:studentId",
        name: "admin-student-application-list",
        component: AdminApplicationListView,
        meta: {
            requiresAuth: true,
            requiredRole: "Admin"
        }
    },
    {
        path: "/admin/students/:studentId/:applicationId",
        name: "admin-student-application-detail",
        component: AdminApplicationDetailView,
        meta: {
            requiresAuth: true,
            requiredRole: "Admin"
        }
    },
    {
        path: "/company/drives",
        name: "company-drive-list",
        component: CompanyDriveListView,
        meta: {
            requiresAuth: true,
            requiredRole: "Company"
        }
    },
    {
        path: "/company/drives/:driveId",
        name: "company-drive-application-list",
        component: CompanyApplicationListView,
        meta: {
            requiresAuth: true,
            requiredRole: "Company"
        }
    },
    {
        path: "/company/drives/:driveId/:applicationId",
        name: "company-drive-application-detail",
        component: CompanyApplicationDetailView,
        meta: {
            requiresAuth: true,
            requiredRole: "Company"
        }
    },
    {
        path: "/student/companies",
        name: "student-company-list",
        component: StudentCompanyListView,
        meta: {
            requiresAuth: true,
            requiredRole: "Student"
        }
    },
    {
        path: "/student/companies/:companyId",
        name: "student-company-drive-list",
        component: StudentDriveListView,
        meta: {
            requiresAuth: true,
            requiredRole: "Student"
        }
    },
    {
        path: "/student/companies/:companyId/:driveId",
        name: "student-company-drive-detail",
        component: StudentDriveDetailView,
        meta: {
            requiresAuth: true,
            requiredRole: "Student"
        }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

router.beforeEach(async (to) => {

    const authStore = useAuthStore()

    const wasLoggedIn = authStore.isLoggedIn

    const sessionValid = await authStore.fetchCurrentUser(true)

    if (!sessionValid && wasLoggedIn) {

        await authStore.handleSessionExpired()

        return false
    
    }

    if (to.meta.guestOnly && authStore.isLoggedIn) {
    
        return {
            name: `${authStore.user.role.toLowerCase()}-dashboard`
        }
    }

    if (to.meta.requiresAuth) {

        if (!authStore.isLoggedIn) {

            return {
                name: `${to.meta.requiredRole.toLowerCase()}-login`
            }
        }

        if (authStore.user.role !== to.meta.requiredRole) {

            return {
                name: `${authStore.user.role.toLowerCase()}-dashboard`
            }
        }

    }

    return true
})

export default router

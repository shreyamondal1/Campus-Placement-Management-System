<template>
    <div class="container py-5 text-center">
        <h1 class="mb-3">Welcome to PlacementConnect</h1>
        <p class="lead mb-5">A centralized placement portal connecting administrator, organizations and candidates.</p>
        <div class="row g-4 justify-content-center">
            <div class="col-md-4">
                <div class="card shadow h-100">
                    <div class="card-body">
                        <h2 class="card-title h4">Admin</h2>
                        <p class="card-text">Manage companies, students, placement drives, job applications and placements.</p>
                        <RouterLink v-bind:to="{ name: 'admin' }" class="btn btn-primary w-50">Admin Portal</RouterLink>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card shadow h-100">
                    <div class="card-body">
                        <h2 class="card-title h4">Company</h2>
                        <p class="card-text">Register your company, create placement drives and manage student applications.</p>
                        <RouterLink v-bind:to="{ name: 'company' }" class="btn btn-primary w-50">Company Portal</RouterLink>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card shadow h-100">
                    <div class="card-body">
                        <h2 class="card-title h4">Student</h2>
                        <p class="card-text">Build your profile, access placement opportunities and track your applications.</p>
                        <RouterLink v-bind:to="{ name: 'student' }" class="btn btn-primary w-50">Student Portal</RouterLink>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

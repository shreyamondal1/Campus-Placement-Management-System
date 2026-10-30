<template>
    <div class="container py-5 text-center">
        <h1 class="mb-3">Company Portal</h1>
        <p class="lead mb-5">Connect with talented students, create placement drives and manage applications throughout the recruitment process.</p>
        <div class="row justify-content-center mt-5">
            <div class="col-auto">
                <div class="card" style="width: 600px; height: 300px;">
                    <div class="card-body p-5">
                        <div class="d-flex h-100 justify-content-center align-items-center gap-3">
                            <RouterLink v-bind:to="{ name: 'company-register' }" class="btn btn-primary px-5 py-2">Register</RouterLink>
                            <RouterLink v-bind:to="{ name: 'company-login' }" class="btn btn-primary px-5 py-2">Login</RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

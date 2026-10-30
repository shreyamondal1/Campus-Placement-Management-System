<template>
    <div class="container py-5 text-center">
        <h1 class="mb-3">Admin Portal</h1>
        <p class="lead mb-5">Manage the PlacementConnect platform, companies, students, and placement process.</p>
        <div class="row justify-content-center mt-5">
            <div class="col-auto">
                <div class="card" style="width: 500px; height: 250px;">
                    <div class="card-body p-5">
                        <div class="d-flex h-100 justify-content-center align-items-center">
                            <RouterLink v-bind:to="{ name: 'admin-login' }" class="btn btn-primary px-5 py-2">Login</RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

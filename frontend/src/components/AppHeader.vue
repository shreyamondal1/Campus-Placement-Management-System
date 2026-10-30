<template>
    <header class="app-header d-flex justify-content-center align-items-center">
        <div class="container">
            <RouterLink v-bind:to="{ name: 'home' }" class="text-white text-decoration-none fs-5 fw-semibold">
                <img src="/src/assets/icons/placementconnect-multicolored.png" class="app-logo me-2">
                PlacementConnect
            </RouterLink>
        </div>
    </header>
</template>

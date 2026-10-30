<template>
    <AppHeader />
    <AppNavbar />
    <AppFlash />
    <main class="main-content flex-grow-1">
        <RouterView />
    </main>
    <AppToast />
    <AppFooter />
</template>

<script setup>
import AppHeader from "./components/AppHeader.vue"
import AppNavbar from "./components/AppNavbar.vue"
import AppFlash from "./components/AppFlash.vue"
import AppToast from "./components/AppToast.vue"
import AppFooter from "./components/AppFooter.vue"
</script>

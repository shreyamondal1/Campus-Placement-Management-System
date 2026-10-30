<template>
    <div v-if="flash.visible" class="container mt-3">
        <div v-bind:class="`alert alert-${flash.type} alert-dismissible fade show`"> {{ flash.message }}
            <button type="button" class="btn-close" v-on:click="flash.clear"></button>
        </div>
    </div>
</template>

<script setup>
import { useFlashStore } from "../stores/flash"

const flash = useFlashStore()
</script>

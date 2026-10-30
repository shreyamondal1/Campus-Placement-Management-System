<template>
    <div v-if="toast.visible" class="toast-container position-fixed bottom-0 end-0 p-3">
        <div class="toast show border-0" v-bind:class="{'bg-info-subtle': toast.type === 'action', 'bg-primary-subtle': toast.type === 'completion'}">
            <div class="toast-body"> {{ toast.message }} </div>
        </div>
    </div>
</template>

<script setup>
import { useToastStore } from "../stores/toast"

const toast = useToastStore()
</script>

<template>
    <div class="container py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-semibold mb-1">Inbox</h2>
        </div>
        <div v-if="errorMessage" class="alert alert-danger"> {{ errorMessage }} </div>
        <div v-if="loading" class="text-center py-5"><div class="spinner-border"></div></div>
        <div v-else class="row g-4">
            <div class="col-md-4">
                <div class="card shadow-sm">
                    <div class="card-header fw-bold">Notifications</div>
                    <div class="list-group list-group-flush">
                        <button v-for="notification in notifications" v-bind:key="notification.notification_filename" type="button" class="list-group-item list-group-item-action text-start" v-bind:class="{active: selectedNotification?.notification_filename === notification.notification_filename}" v-on:click="selectNotification(notification)">
                            <div class="d-flex justify-content-between"><strong class="text-truncate"> {{ notification.notification_subject }} </strong></div>
                            <small v-bind:class="selectedNotification?.notification_filename === notification.notification_filename? 'text-white-50' : 'text-muted'"> {{ notification.notification_sent }} </small>
                        </button>
                        <div v-if="notifications.length === 0" class="p-4 text-center text-muted">No notifications.</div>
                    </div>
                </div>
            </div>
            <div class="col-md-8">
                <div class="card shadow-sm">
                    <div v-if="!selectedNotification" class="card-body text-center text-muted py-5"><i class="bi bi-envelope fs-1"></i><p class="mt-3 mb-0">Select a notification to view it.</p></div>
                    <div v-else>
                        <div class="card-header">
                            <h5 class="fw-bold mb-1"> {{ selectedNotification.notification_subject }} </h5>
                            <small class="text-muted">Sent: {{ selectedNotification.notification_sent }} </small>
                        </div>
                        <div class="card-body">
                            <div v-html="notificationDetail.notification_body"></div>
                            <div v-if="notificationDetail.attachment_filename" class="mt-4">
                                <h6 class="fw-bold mb-3">Attachment</h6>
                                <div class="d-flex justify-content-between align-items-center border rounded p-3">
                                    <div><i class="bi bi-paperclip me-2"></i> {{ notificationDetail.attachment_filename }} </div>
                                    <button type="button" class="btn btn-sm btn-outline-primary" v-on:click="downloadAttachment(notificationDetail.attachment_filename)"><i class="bi bi-download me-1"></i>Download</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

import { getCompanyInbox, getCompanyInboxNotification, getCompanyInboxNotificationAttachment } from "../../services/company"

const notifications = ref([])
const selectedNotification = ref(null)
const notificationDetail = ref({})
const loading = ref(true)
const errorMessage = ref("")

async function loadInbox() {

    loading.value = true
    errorMessage.value = ""

    try {

        notifications.value = await getCompanyInbox()

    } catch (error) {

        errorMessage.value = error.response?.data?.message || "Failed to load inbox."

    } finally {

        loading.value = false

    }

}

async function selectNotification(notification) {

    selectedNotification.value = notification
    notificationDetail.value = {}
    errorMessage.value = ""

    try {

        notificationDetail.value = await getCompanyInboxNotification(notification.notification_filename)

    } catch (error) {

        errorMessage.value = error.response?.data?.message || "Failed to load notification."

    }

}

async function downloadAttachment(attachmentFilename) {

    try {

        const blob = await getCompanyInboxNotificationAttachment(selectedNotification.value.notification_filename, attachmentFilename)

        const url = window.URL.createObjectURL(blob)

        const link = document.createElement("a")

        link.href = url
        link.download = attachmentFilename

        document.body.appendChild(link)

        link.click()

        link.remove()

        window.URL.revokeObjectURL(url)

    } catch (error) {

        errorMessage.value = error.response?.data?.message || "Failed to download attachment."
        
    }

}

onMounted(loadInbox)
</script>

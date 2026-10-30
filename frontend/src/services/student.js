import api from "./api"

export async function getStudentDashboard() {
    const response = await api.get("/student/dashboard")
    return response.data
}

export async function getStudentCompanies() {
    const response = await api.get("/student/companies")
    return response.data
}

export async function getStudentCompanyDrives(companyId) {
    const response = await api.get(`/student/companies/${companyId}/drives`)
    return response.data
}

export async function getStudentCompanyDriveData(companyId, driveId) {
    const response = await api.get(`/student/companies/${companyId}/drives/${driveId}`)
    return response.data
}

export async function studentApplyDrive(driveId) {
    const response = await api.post(`/student/drives/${driveId}/apply`)
    return response.data
}

export async function studentWithdrawDrive(driveId) {
    const response = await api.delete(`/student/drives/${driveId}/withdraw`)
    return response.data
}

export async function getStudentProfile() {
    const response = await api.get("/student/profile")
    return response.data
}

export async function updateStudentProfile(data) {
    const response = await api.put("/student/profile", data)
    return response.data
}

export async function deleteStudentProfile() {
    const response = await api.delete("/student/profile")
    return response.data
}

export async function exportStudentProfile() {
    const response = await api.post("/student/profile/export")
    return response.data
}

export async function getStudentInbox() {
    const response = await api.get("/student/inbox")
    return response.data
}

export async function getStudentInboxNotification(notificationFilename) {
    const response = await api.get(`/student/inbox/notification/${notificationFilename}`)
    return response.data
}

export async function getStudentInboxNotificationAttachment(notificationFilename, attachmentFilename) {
    const response = await api.get(`/student/inbox/notification/${notificationFilename}/attachment/${attachmentFilename}`, {responseType: "blob"})
    return response.data
}

export async function getStudentInboxStatus() {
    const response = await api.get("/student/inbox/status")
    return response.data
}

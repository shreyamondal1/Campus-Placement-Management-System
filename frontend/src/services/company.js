import api from "./api"

export async function getCompanyDashboard() {
    const response = await api.get("/company/dashboard")
    return response.data
}

export async function getCompanyDrives() {
    const response = await api.get("/company/drives")
    return response.data
}

export async function getCompanyDriveApplications(driveId) {
    const response = await api.get(`/company/drives/${driveId}/applications`)
    return response.data
}

export async function getCompanyDriveApplicationData(driveId, applicationId) {
    const response = await api.get(`/company/drives/${driveId}/applications/${applicationId}`)
    return response.data
}

export async function companyCreateDrive(data) {
    const response = await api.post("/company/drives/create", data)
    return response.data
}

export async function companyUpdateDrive(driveId, data) {
    const response = await api.put(`/company/drives/${driveId}/update`, data)
    return response.data
}

export async function companyDeleteDrive(driveId) {
    const response = await api.delete(`/company/drives/${driveId}/delete`)
    return response.data
}

export async function companyUpdateApplication(applicationId, data) {
    const response = await api.put(`/company/applications/${applicationId}/update`, data)
    return response.data
}

export async function getCompanyProfile() {
    const response = await api.get("/company/profile")
    return response.data
}

export async function updateCompanyProfile(data) {
    const response = await api.put("/company/profile", data)
    return response.data
}

export async function deleteCompanyProfile() {
    const response = await api.delete("/company/profile")
    return response.data
}

export async function exportCompanyProfile() {
    const response = await api.post("/company/profile/export")
    return response.data
}

export async function getCompanyInbox() {
    const response = await api.get("/company/inbox")
    return response.data
}

export async function getCompanyInboxNotification(notificationFilename) {
    const response = await api.get(`/company/inbox/notification/${notificationFilename}`)
    return response.data
}

export async function getCompanyInboxNotificationAttachment(notificationFilename, attachmentFilename) {
    const response = await api.get(`/company/inbox/notification/${notificationFilename}/attachment/${attachmentFilename}`, {responseType: "blob"})
    return response.data
}

export async function getCompanyInboxStatus() {
    const response = await api.get("/company/inbox/status")
    return response.data
}

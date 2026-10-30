import api from "./api"

export async function getAdminDashboard() {
    const response = await api.get("/admin/dashboard")
    return response.data
}

export async function getAdminCompanies() {
    const response = await api.get("/admin/companies")
    return response.data
}

export async function getAdminStudents() {
    const response = await api.get("/admin/students")
    return response.data
}

export async function getAdminCompanyDrives(companyId) {
    const response = await api.get(`/admin/companies/${companyId}/drives`)
    return response.data
}

export async function getAdminCompanyDriveApplications(companyId, driveId) {
    const response = await api.get(`/admin/companies/${companyId}/drives/${driveId}/applications`)
    return response.data
}

export async function getAdminStudentApplications(studentId) {
    const response = await api.get(`/admin/students/${studentId}/applications`)
    return response.data
}

export async function getAdminApplicationData(applicationId) {
    const response = await api.get(`/admin/applications/${applicationId}`)
    return response.data
}

export async function adminApproveCompany(companyId) {
    const response = await api.post(`/admin/companies/${companyId}/approve`)
    return response.data
}

export async function adminRejectCompany(companyId) {
    const response = await api.post(`/admin/companies/${companyId}/reject`)
    return response.data
}

export async function adminReapproveCompany(companyId) {
    const response = await api.post(`/admin/companies/${companyId}/reapprove`)
    return response.data
}

export async function adminDisableCompany(companyId) {
    const response = await api.post(`/admin/companies/${companyId}/disable`)
    return response.data
}

export async function adminEnableCompany(companyId) {
    const response = await api.post(`/admin/companies/${companyId}/enable`)
    return response.data
}

export async function adminBlacklistCompany(companyId) {
    const response = await api.post(`/admin/companies/${companyId}/blacklist`)
    return response.data
}

export async function adminWhitelistCompany(companyId) {
    const response = await api.post(`/admin/companies/${companyId}/whitelist`)
    return response.data
}

export async function adminDeleteCompany(companyId) {
    const response = await api.delete(`/admin/companies/${companyId}/delete`)
    return response.data
}

export async function adminDisableStudent(studentId) {
    const response = await api.post(`/admin/students/${studentId}/disable`)
    return response.data
}

export async function adminEnableStudent(studentId) {
    const response = await api.post(`/admin/students/${studentId}/enable`)
    return response.data
}

export async function adminBlacklistStudent(studentId) {
    const response = await api.post(`/admin/students/${studentId}/blacklist`)
    return response.data
}

export async function adminWhitelistStudent(studentId) {
    const response = await api.post(`/admin/students/${studentId}/whitelist`)
    return response.data
}

export async function adminDeleteStudent(studentId) {
    const response = await api.delete(`/admin/students/${studentId}/delete`)
    return response.data
}

export async function adminApproveDrive(driveId) {
    const response = await api.post(`/admin/drives/${driveId}/approve`)
    return response.data
}

export async function adminRejectDrive(driveId) {
    const response = await api.post(`/admin/drives/${driveId}/reject`)
    return response.data
}

export async function adminReapproveDrive(driveId) {
    const response = await api.post(`/admin/drives/${driveId}/reapprove`)
    return response.data
}

export async function getAdminProfile() {
    const response = await api.get("/admin/profile")
    return response.data
}

export async function updateAdminProfile(data) {
    const response = await api.put("/admin/profile", data)
    return response.data
}

export async function exportAdminProfile() {
    const response = await api.post("/admin/profile/export")
    return response.data
}

export async function getAdminInbox() {
    const response = await api.get("/admin/inbox")
    return response.data
}

export async function getAdminInboxNotification(notificationFilename) {
    const response = await api.get(`/admin/inbox/notification/${notificationFilename}`)
    return response.data
}

export async function getAdminInboxNotificationAttachment(notificationFilename, attachmentFilename) {
    const response = await api.get(`/admin/inbox/notification/${notificationFilename}/attachment/${attachmentFilename}`, {responseType: "blob"})
    return response.data
}

export async function getAdminInboxStatus() {
    const response = await api.get("/admin/inbox/status")
    return response.data
}

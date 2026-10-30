<template>
    <div class="container py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-semibold mb-1">Profile</h2>
            <button class="btn btn-primary" type="button" v-on:click="exportData" v-bind:disabled="exporting"><i class="bi bi-download me-2"></i> {{ exporting ? "Generating..." : "Export Data" }} </button>
        </div>
        <div v-if="loading" class="text-center py-5"><div class="spinner-border"></div></div>
        <div v-else-if="error" class="alert alert-danger"> {{ error }} </div>
        <div v-else>
            <div class="card shadow-sm">
                <div class="card-body">
                    <h5 class="fw-semibold mb-4">Account Information</h5>
                    <div v-if="!editing">
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Username</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.username }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Email</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.email }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Name</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.name }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Contact Number</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.contact_number }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Degree</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.degree }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Department</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.department }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Graduation Year</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.graduation_year }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">CGPA</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.cgpa }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Skills</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.skills || "-" }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Certifications</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.certifications || "-" }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Achievements</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.achievements || "-" }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">LinkedIn</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.linkedin || "-" }} </p></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">GitHub</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.github || "-" }} </p>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Portfolio</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.portfolio || "-" }} </p></div>
                        </div>
                        <div class="row mb-4">
                            <label class="col-sm-3 col-form-label fw-semibold">Resume</label>
                            <div class="col-sm-9"><p class="form-control-plaintext"> {{ profile.resume }} </p></div>
                        </div>
                        <h6 class="fw-semibold mb-3">Education</h6>
                        <div v-if="educations.length === 0" class="text-muted mb-4">No education details added.</div>
                        <div v-for="education in educations" v-bind:key="education.id" class="border rounded p-3 mb-3">
                            <div class="row mb-2">
                                <label class="col-sm-3 fw-semibold">Degree</label>
                                <div class="col-sm-9"> {{ education.degree }} </div>
                            </div>
                            <div class="row mb-2">
                                <label class="col-sm-3 fw-semibold">Institution</label>
                                <div class="col-sm-9"> {{ education.institution }} </div>
                            </div>
                            <div class="row mb-2">
                                <label class="col-sm-3 fw-semibold">Start Date</label>
                                <div class="col-sm-9"> {{ education.start_date }} </div>
                            </div>
                            <div class="row mb-2">
                                <label class="col-sm-3 fw-semibold">End Date</label>
                                <div class="col-sm-9"> {{ education.end_date }} </div>
                            </div>
                            <div class="row">
                                <label class="col-sm-3 fw-semibold">Coursework</label>
                                <div class="col-sm-9"> {{ education.coursework }} </div>
                            </div>
                        </div>
                        <h6 class="fw-semibold mt-4 mb-3">Experience</h6>
                        <div v-if="experiences.length === 0" class="text-muted mb-4">No experience details added.</div>
                        <div v-for="experience in experiences" v-bind:key="experience.id" class="border rounded p-3 mb-3">
                            <div class="row mb-2">
                                <label class="col-sm-3 fw-semibold">Role</label>
                                <div class="col-sm-9"> {{ experience.role }} </div>
                            </div>
                            <div class="row mb-2">
                                <label class="col-sm-3 fw-semibold">Organization</label>
                                <div class="col-sm-9"> {{ experience.organization }} </div>
                            </div>
                            <div class="row mb-2">
                                <label class="col-sm-3 fw-semibold">Start Date</label>
                                <div class="col-sm-9"> {{ experience.start_date }} </div>
                            </div>
                            <div class="row mb-2">
                                <label class="col-sm-3 fw-semibold">End Date</label>
                                <div class="col-sm-9"> {{ experience.end_date }}
                                </div>
                            </div>
                            <div class="row">
                                <label class="col-sm-3 fw-semibold">Description</label>
                                <div class="col-sm-9"> {{ experience.description }} </div>
                            </div>
                        </div>
                        <h6 class="fw-semibold mt-4 mb-3">Project</h6>
                        <div v-if="projects.length === 0" class="text-muted mb-4">No projects added.</div>
                        <div v-for="project in projects" v-bind:key="project.id" class="border rounded p-3 mb-3">
                            <div class="row mb-2">
                                <label class="col-sm-3 fw-semibold">Name</label>
                                <div class="col-sm-9"> {{ project.name }} </div>
                            </div>
                            <div class="row mb-2">
                                <label class="col-sm-3 fw-semibold">Link</label>
                                <div class="col-sm-9"> {{ project.link }} </div>
                            </div>
                            <div class="row">
                                <label class="col-sm-3 fw-semibold">Description</label>
                                <div class="col-sm-9"> {{ project.description }} </div>
                            </div>
                        </div>
                        <div class="mt-4">
                            <button type="button" class="btn btn-primary" v-on:click="startEditing"><i class="bi bi-pencil me-2"></i>Edit Profile</button>
                            <button type="button" class="btn btn-danger ms-2" v-on:click="deleteProfile" v-bind:disabled="deleting"><i class="bi bi-trash me-2"></i> {{ deleting ? "Deleting..." : "Delete Profile" }} </button>
                        </div>
                    </div>
                    <form v-else v-on:submit.prevent="updateProfile">
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Username</label>
                            <div class="col-sm-9"><input v-model="editProfile.username" type="text" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Email</label>
                            <div class="col-sm-9"><input v-model="editProfile.email" type="email" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Password</label>
                            <div class="col-sm-9"><input v-model="editProfile.password" type="password" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Name</label>
                            <div class="col-sm-9"><input v-model="editProfile.name" type="text" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Contact Number</label>
                            <div class="col-sm-9"><input v-model="editProfile.contact_number" type="text" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Degree</label>
                            <div class="col-sm-9"><input v-model="editProfile.degree" type="text" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Department</label>
                            <div class="col-sm-9"><input v-model="editProfile.department" type="text" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Graduation Year</label>
                            <div class="col-sm-9"><input v-model.number="editProfile.graduation_year" type="number" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">CGPA</label>
                            <div class="col-sm-9"><input v-model.number="editProfile.cgpa" type="number" step="0.01" class="form-control" required></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Skills</label>
                            <div class="col-sm-9"><textarea v-model="editProfile.skills" class="form-control" rows="2"></textarea></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Certifications</label>
                            <div class="col-sm-9"><textarea v-model="editProfile.certifications" class="form-control" rows="2"></textarea></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Achievements</label>
                            <div class="col-sm-9"><textarea v-model="editProfile.achievements" class="form-control" rows="2"></textarea></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">LinkedIn</label>
                            <div class="col-sm-9"><input v-model="editProfile.linkedin" type="url" class="form-control"></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">GitHub</label>
                            <div class="col-sm-9"><input v-model="editProfile.github" type="url" class="form-control"></div>
                        </div>
                        <div class="row mb-3">
                            <label class="col-sm-3 col-form-label fw-semibold">Portfolio</label>
                            <div class="col-sm-9"><input v-model="editProfile.portfolio" type="url" class="form-control"></div>
                        </div>
                        <div class="row mb-4">
                            <label class="col-sm-3 col-form-label fw-semibold">Resume</label>
                            <div class="col-sm-9"><input v-model="editProfile.resume" type="url" class="form-control" required></div>
                        </div>
                        <h6 class="fw-semibold mt-4 mb-3">Education</h6>
                        <div v-for="(education, index) in editEducations" v-bind:key="education.id || `education-${index}`" class="border rounded p-3 mb-3">
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">Degree</label>
                                <div class="col-sm-9"><input v-model="education.degree" type="text" class="form-control" required></div>
                            </div>
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">Institution</label>
                                <div class="col-sm-9"><input v-model="education.institution" type="text" class="form-control" required></div>
                            </div>
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">Start Date</label>
                                <div class="col-sm-9"><input v-model="education.start_date" type="date" class="form-control"required></div>
                            </div>
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">End Date</label>
                                <div class="col-sm-9"><input v-model="education.end_date" type="date" class="form-control" required></div>
                            </div>
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">Coursework</label>
                                <div class="col-sm-9"><textarea v-model="education.coursework" class="form-control" rows="2" required></textarea></div>
                            </div>
                            <button type="button" class="btn btn-outline-danger btn-sm" v-on:click="removeEducation(index)"><i class="bi bi-trash me-1"></i>Remove</button>
                        </div>
                        <button type="button" class="btn btn-outline-primary btn-sm mb-4" v-on:click="addEducation"><i class="bi bi-plus me-1"></i>Add Education</button>
                        <h6 class="fw-semibold mt-4 mb-3">Experience</h6>
                        <div v-for="(experience, index) in editExperiences" v-bind:key="experience.id || `experience-${index}`" class="border rounded p-3 mb-3">
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">Role</label>
                                <div class="col-sm-9"><input v-model="experience.role" type="text" class="form-control" required></div>
                            </div>
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">Organization</label>
                                <div class="col-sm-9"><input v-model="experience.organization" type="text" class="form-control" required></div>
                            </div>
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">Start Date</label>
                                <div class="col-sm-9"><input v-model="experience.start_date" type="date" class="form-control" required></div>
                            </div>
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">End Date</label>
                                <div class="col-sm-9"><input v-model="experience.end_date" type="date" class="form-control" required></div>
                            </div>
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">Description</label>
                                <div class="col-sm-9"><textarea v-model="experience.description" class="form-control" rows="2" required></textarea></div>
                            </div>
                            <button type="button" class="btn btn-outline-danger btn-sm" v-on:click="removeExperience(index)"><i class="bi bi-trash me-1"></i>Remove</button>
                        </div>
                        <button type="button" class="btn btn-outline-primary btn-sm mb-4" v-on:click="addExperience"><i class="bi bi-plus me-1"></i>Add Experience</button>
                        <h6 class="fw-bold mt-4 mb-3">Project</h6>
                        <div v-for="(project, index) in editProjects" v-bind:key="project.id || `project-${index}`" class="border rounded p-3 mb-3">
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">Name</label>
                                <div class="col-sm-9"><input v-model="project.name" type="text" class="form-control" required></div>
                            </div>
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">Link</label>
                                <div class="col-sm-9"><input v-model="project.link" type="url" class="form-control" required></div>
                            </div>
                            <div class="row mb-3">
                                <label class="col-sm-3 col-form-label fw-semibold">Description</label>
                                <div class="col-sm-9"><textarea v-model="project.description" class="form-control" rows="2" required></textarea></div>
                            </div>
                            <button type="button" class="btn btn-outline-danger btn-sm" v-on:click="removeProject(index)"><i class="bi bi-trash me-1"></i>Remove</button>
                        </div>
                        <button type="button" class="btn btn-outline-primary btn-sm mb-4" v-on:click="addProject"><i class="bi bi-plus me-1"></i>Add Project</button>
                        <div class="mt-3">
                            <button type="submit" class="btn btn-success" v-bind:disabled="saving"> {{ saving ? "Saving..." : "Save Changes" }} </button>
                            <button type="button" class="btn btn-secondary ms-2" v-on:click="cancelEditing" v-bind:disabled="saving">Cancel</button>
                        </div>
                    </form>
                    <div v-if="showConfirm" class="modal fade show" style="display:block; background-color:rgba(0,0,0,.5);">
                        <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Confirm Action</h5>
                                </div>
                                <div class="modal-body"> {{ confirmMessage }} </div>
                                <div class="modal-footer">
                                    <button class="btn btn-success" v-on:click="cancelAction">Cancel</button>
                                    <button class="btn btn-danger" v-on:click="confirmAction">Confirm</button>
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
import { ref, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"

import { getStudentProfile, updateStudentProfile, deleteStudentProfile, exportStudentProfile, getStudentInboxStatus } from "../../services/student"

import { useToastStore } from "../../stores/toast"

const router = useRouter()
const toast = useToastStore()

const profile = ref({
    username: "",
    email: "",
    name: "",
    contact_number: "",
    degree: "",
    department: "",
    graduation_year: null,
    cgpa: null,
    skills: "",
    certifications: "",
    achievements: "",
    linkedin: "",
    github: "",
    portfolio: "",
    resume: ""
})

const educations = ref([])
const experiences = ref([])
const projects = ref([])

const editProfile = ref({})
const editEducations = ref([])
const editExperiences = ref([])
const editProjects = ref([])

const error = ref("")
const loading = ref(false)
const editing = ref(false)
const saving = ref(false)
const exporting = ref(false)
const deleting = ref(false)

const successMessage = ref("")
const errorMessage = ref("")

let notificationInterval = null

const showConfirm = ref(false)
const confirmMessage = ref("")
const pendingAction = ref(null)

async function loadProfile() {

    loading.value = true
    error.value = ""

    try {

        const data = await getStudentProfile()

        profile.value = data.profile
        educations.value = data.educations
        experiences.value = data.experiences
        projects.value = data.projects

    } catch (err) {

        error.value = err.response?.data?.message || "Failed to load profile."

    } finally {

        loading.value = false

    }

}

function startEditing() {

    editProfile.value = {
        username: profile.value.username,
        email: profile.value.email,
        password: "",
        name: profile.value.name,
        contact_number: profile.value.contact_number,
        degree: profile.value.degree,
        department: profile.value.department,
        graduation_year: profile.value.graduation_year,
        cgpa: profile.value.cgpa,
        skills: profile.value.skills || "",
        certifications: profile.value.certifications || "",
        achievements: profile.value.achievements || "",
        linkedin: profile.value.linkedin || "",
        github: profile.value.github || "",
        portfolio: profile.value.portfolio || "",
        resume: profile.value.resume
    }

    editEducations.value = educations.value.map(education => ({
        ...education
    }))

    editExperiences.value = experiences.value.map(experience => ({
        ...experience
    }))

    editProjects.value = projects.value.map(project => ({
        ...project
    }))

    successMessage.value = ""
    errorMessage.value = ""
    editing.value = true

}

function cancelEditing() {

    editing.value = false
    errorMessage.value = ""

}

function addEducation() {

    editEducations.value.push({
        degree: "",
        institution: "",
        start_date: "",
        end_date: "",
        coursework: ""
    })

}

function removeEducation(index) {

    editEducations.value.splice(index, 1)

}

function addExperience() {

    editExperiences.value.push({
        role: "",
        organization: "",
        start_date: "",
        end_date: "",
        description: ""
    })

}

function removeExperience(index) {

    editExperiences.value.splice(index, 1)

}

function addProject() {

    editProjects.value.push({
        name: "",
        link: "",
        description: ""
    })

}

function removeProject(index) {

    editProjects.value.splice(index, 1)

}

async function updateProfile() {

    saving.value = true
    successMessage.value = ""
    errorMessage.value = ""

    try {

        const data = await updateStudentProfile({

            profile_update: {
                username: editProfile.value.username,
                email: editProfile.value.email,
                password: editProfile.value.password,
                name: editProfile.value.name,
                contact_number: editProfile.value.contact_number,
                degree: editProfile.value.degree,
                department: editProfile.value.department,
                graduation_year: editProfile.value.graduation_year,
                cgpa: editProfile.value.cgpa,
                skills: editProfile.value.skills || null,
                certifications: editProfile.value.certifications || null,
                achievements: editProfile.value.achievements || null,
                linkedin: editProfile.value.linkedin || null,
                github: editProfile.value.github || null,
                portfolio: editProfile.value.portfolio || null,
                resume: editProfile.value.resume
            },

            educations: editEducations.value,
            experiences: editExperiences.value,
            projects: editProjects.value
        })

        profile.value = data.profile
        educations.value = data.educations
        experiences.value = data.experiences
        projects.value = data.projects

        editing.value = false

        successMessage.value = "Profile updated successfully."

        toast.completion(successMessage)

    } catch (err) {

        errorMessage.value = err.response?.data?.message || "Failed to update profile."

        toast.completion(errorMessage)

    } finally {

        saving.value = false

    }

}

async function exportData() {

    exporting.value = true
    successMessage.value = ""
    errorMessage.value = ""

    try {

        const data = await exportStudentProfile()

        successMessage.value = data.message || "Export generation started. You will be notified when it is ready."

        toast.completion(successMessage)

    } catch (err) {

        errorMessage.value = err.response?.data?.message || "Failed to start export."

        toast.completion(errorMessage)

    } finally {

        exporting.value = false

    }

}

async function checkNotificationStatus() {

    try {

        const status = await getStudentInboxStatus()

        if (status.task_completed) {

            toast.completion(status.message)

        }

    } catch (err) {

        error.value = err.response?.data?.message || "Failed to check notification status"

    }

}

function deleteProfile() {

    openConfirm("Are you sure you want to delete your account?", confirmDeleteProfile)

}

async function confirmDeleteProfile() {

    deleting.value = true
    successMessage.value = ""
    errorMessage.value = ""

    try {

        await deleteStudentProfile()

        await router.push({name: "home"})

    } catch (err) {

        errorMessage.value = err.response?.data?.message || "Failed to delete profile."

        toast.completion(errorMessage)

    } finally {

        deleting.value = false

    }

}

function openConfirm(message, action) {

    showConfirm.value = true
    confirmMessage.value = message
    pendingAction.value = action

}

async function confirmAction() {

    showConfirm.value = false

    if (pendingAction.value) {
        await pendingAction.value()
        pendingAction.value = null
    }

}

function cancelAction() {

    showConfirm.value = false
    pendingAction.value = null

}

onMounted(() => {

    loadProfile()

    checkNotificationStatus()

    notificationInterval = setInterval(checkNotificationStatus, 100)

})

onUnmounted(() => {

    clearInterval(notificationInterval)

})

</script>

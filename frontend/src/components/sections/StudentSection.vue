<script setup>
defineProps({
    student: {
        type: Object,
        required: true
    },
    mode: {
        type: String,
        required: true
    }
})
</script>

<template>
    <div class="card shadow-sm">
        <div class="card-header bg-primary-subtle">
            <h5 class="mb-0"><i class="bi bi-mortarboard-fill me-2"></i>Student</h5>
        </div>
        <div class="card-body">
            <h6 class="fw-semibold mb-3">Summary</h6>
            <div class="row g-3 mb-4">
                <div class="col-md-6">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Name</div>
                        <div class="fw-semibold mt-2"> {{ student.name }} </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Email</div>
                        <div class="fw-semibold mt-2"> {{ student.email }} </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Contact Number</div>
                        <div class="fw-semibold mt-2"> {{ student.contact_number }} </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Degree</div>
                        <div class="fw-semibold mt-2"> {{ student.degree }} </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Department</div>
                        <div class="fw-semibold mt-2"> {{ student.department }} </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Graduation Year</div>
                        <div class="fw-semibold mt-2"> {{ student.graduation_year }} </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">CGPA</div>
                        <div class="fw-semibold mt-2"> {{ student.cgpa }} </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Profiles</div>
                        <div class="row g-2">
                            <div class="col-6 col-lg-3">
                                <a v-bind:href="student.linkedin" class="btn btn-outline-primary w-100 mt-2"><i class="bi bi-linkedin me-2"></i>LinkedIn</a>
                            </div>
                            <div class="col-6 col-lg-3">
                                <a v-bind:href="student.github" class="btn btn-outline-primary w-100 mt-2"><i class="bi bi-github me-2"></i>GitHub</a>
                            </div>
                            <div class="col-6 col-lg-3">
                                <a v-bind:href="student.portfolio" class="btn btn-outline-primary w-100 mt-2"><i class="bi-person-vcard-fill me-2"></i>Portfolio</a>
                            </div>
                            <div class="col-6 col-lg-3">
                                <a v-bind:href="student.resume" class="btn btn-outline-primary w-100 mt-2"><i class="bi bi-file-earmark-pdf-fill me-2"></i>Resume</a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="border rounded p-3 h-100">
                        <div class="text-muted small">Student Status</div>
                        <span class="badge mt-2" v-bind:class="{
                            'text-bg-success': student.user_status === 'Active',
                            'text-bg-warning': student.user_status === 'Disabled',
                            'text-bg-dark': student.user_status === 'Blacklisted'
                        }"> {{ student.user_status }} </span>
                    </div>
                </div>
            </div>
            <hr>
            <h6 class="fw-semibold mb-3">Skills</h6>
            <div class="mb-4">
                <span v-for="skill in (student.skills?.split(',') ?? ['-'])" v-bind:key="skill" class="badge border border-dark text-dark me-2 mb-2 px-3 py-2"> {{ skill.trim() }} </span>
            </div>
            <h6 class="fw-semibold mb-3">Certifications</h6>
            <div class="mb-4">
                <span v-for="certification in (student.certifications?.split(',') ?? ['-'])" v-bind:key="certification" class="badge border border-dark text-dark me-2 mb-2 px-3 py-2"> {{ certification.trim() }} </span>
            </div>
            <h6 class="fw-semibold mb-3">Achievements</h6>
            <div class="mb-4">
                <span v-for="achievement in (student.achievements?.split(',') ?? ['-'])" v-bind:key="achievement" class="badge border border-dark text-dark me-2 mb-2 px-3 py-2"> {{ achievement.trim() }} </span>
            </div>
            <hr>
            <h6 class="fw-semibold mb-3">Education</h6>
            <div v-for="education in student.educations" v-bind:key="education.id" class="card border mb-3">
                <div class="card-body">
                    <div class="d-flex justify-content-between flex-wrap">
                        <div class="fw-bold"> {{ education.institution }} </div>
                        <span class="badge text-dark"> {{ education.duration }} </span>
                    </div>
                    <div class="mt-2"> {{ education.degree }} </div>
                    <div>
                        <div class="fw-bold mt-2">Coursework:</div>
                        <div> {{ education.coursework }} </div>
                    </div>
                </div>
            </div>
            <hr>
            <h6 class="fw-semibold mb-3">Experience</h6>
            <div v-for="experience in student.experiences" v-bind:key="experience.id" class="card border mb-3">
                <div class="card-body">
                    <div class="d-flex justify-content-between flex-wrap">
                        <div class="fw-bold"> {{ experience.organization }} </div>
                        <span class="badge text-dark"> {{ experience.tenure }} </span>
                    </div>
                    <div class="mt-2"> {{ experience.role }} </div>
                    <div>
                        <div class="fw-bold mt-2">Responsibilities:</div>
                        <div> {{ experience.description }} </div>
                    </div>
                </div>
            </div>
            <hr>
            <h6 class="fw-semibold mb-3">Project</h6>
            <div v-for="project in student.projects" v-bind:key="project.id" class="card border mb-3">
                <div class="card-body">
                    <div class="d-flex justify-content-between flex-wrap">
                        <div class="fw-bold"> {{ project.name }} </div>
                        <a v-bind:href="project.link" class="btn btn-outline-primary"><i class="bi bi-box-arrow-up-right me-2"></i>View</a>
                    </div>
                    <div> {{ project.description }} </div>
                </div>
            </div>
        </div>
    </div>
</template>

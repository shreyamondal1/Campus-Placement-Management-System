import api from "./api"

export function registerUser(data) {
    return api.post("/auth/register", data)
}

export function loginUser(data) {
    return api.post("/auth/login", data)
}

export function logoutUser() {
    return api.post("/auth/logout")
}

export function getCurrentUser() {
    return api.get("/auth/current_user")
}

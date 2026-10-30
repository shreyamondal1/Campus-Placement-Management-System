import { defineStore } from "pinia"
import { ref } from "vue"

export const useFlashStore = defineStore("flash", () => {

    const visible = ref(false)
    const type = ref("")
    const message = ref("")

    let timeoutId = null

    function show(flashType, flashMessage, duration = 2000) {

        type.value = flashType
        message.value = flashMessage
        visible.value = true

        clearTimeout(timeoutId)

        timeoutId = setTimeout(() => {

            clear()
        
        }, duration)
    }

    function success(message, duration) {
        show("success", message, duration)
    }

    function error(message, duration) {
        show("danger", message, duration)
    }

    function warning(message, duration) {
        show("warning", message, duration)
    }

    function info(message, duration) {
        show("info", message, duration)
    }

    function clear() {
        visible.value = false
        type.value = ""
        message.value = ""
    }

    return {
        visible,
        type,
        message,
        success,
        error,
        warning,
        info,
        clear
    }

})

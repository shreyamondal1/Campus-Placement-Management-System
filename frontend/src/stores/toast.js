import { defineStore } from "pinia"
import { ref } from "vue"

export const useToastStore = defineStore("toast", () => {

    const visible = ref(false)
    const type = ref("")
    const message = ref("")

    let timer = null

    function show(toastType, toastMessage, duration = 1500) {

        type.value = toastType
        message.value = toastMessage
        visible.value = true

        clearTimeout(timer)

        timer = setTimeout(() => {

            visible.value = false

        }, duration)

    }

    function action(message, duration) {
        show("action", message, duration)
    }

    function completion(message, duration) {
        show("completion", message, duration)
    }

    return {
        visible,
        type,
        message,
        action,
        completion
    }

})

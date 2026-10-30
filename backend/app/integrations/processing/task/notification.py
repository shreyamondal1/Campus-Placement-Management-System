from app.integrations.processing.cache.redis import get_cache, set_cache, clear_cache

ADMIN_NOTIFICATION = "notification:admin"
COMPANY_NOTIFICATION = "notification:company:{}"
STUDENT_NOTIFICATION = "notification:student:{}"

def get_admin_notification_cache():

    return get_cache(ADMIN_NOTIFICATION)

def set_admin_notification_cache(message):

    set_cache(ADMIN_NOTIFICATION, {"task_completed": True, "message": message})

def clear_admin_notification_cache():

    clear_cache(ADMIN_NOTIFICATION)

def get_company_notification_cache(company_id):

    return get_cache(COMPANY_NOTIFICATION.format(company_id))

def set_company_notification_cache(company_id, message):

    set_cache(COMPANY_NOTIFICATION.format(company_id), {"task_completed": True, "message": message})

def clear_company_notification_cache(company_id):

    clear_cache(COMPANY_NOTIFICATION.format(company_id))

def get_student_notification_cache(student_id):

    return get_cache(STUDENT_NOTIFICATION.format(student_id))

def set_student_notification_cache(student_id, message):

    set_cache(STUDENT_NOTIFICATION.format(student_id), {"task_completed": True, "message": message})

def clear_student_notification_cache(student_id):

    clear_cache(STUDENT_NOTIFICATION.format(student_id))

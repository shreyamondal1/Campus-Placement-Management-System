from app.integrations.processing.cache.redis import get_cache, set_cache, clear_cache, clear_cache_pattern

ADMIN_DASHBOARD = "dashboard:admin"
COMPANY_DASHBOARD = "dashboard:company:{}"
STUDENT_DASHBOARD = "dashboard:student:{}"
ALL_COMPANY_DASHBOARD = "dashboard:company:*"
ALL_STUDENT_DASHBOARD = "dashboard:student:*"

def get_admin_dashboard_cache():
    
    return get_cache(ADMIN_DASHBOARD)

def set_admin_dashboard_cache(data):

    set_cache(ADMIN_DASHBOARD, data)

def clear_admin_dashboard_cache():

    clear_cache(ADMIN_DASHBOARD)

def get_company_dashboard_cache(company_id):

    return get_cache(COMPANY_DASHBOARD.format(company_id))

def set_company_dashboard_cache(company_id, data):

    set_cache(COMPANY_DASHBOARD.format(company_id), data)

def clear_company_dashboard_cache(company_id):

    clear_cache(COMPANY_DASHBOARD.format(company_id))

def get_student_dashboard_cache(student_id):
    
    return get_cache(STUDENT_DASHBOARD.format(student_id))

def set_student_dashboard_cache(student_id, data):

    set_cache(STUDENT_DASHBOARD.format(student_id), data)

def clear_student_dashboard_cache(student_id):

    clear_cache(STUDENT_DASHBOARD.format(student_id))

def clear_all_company_dashboard_cache():

    clear_cache_pattern(ALL_COMPANY_DASHBOARD)

def clear_all_student_dashboard_cache():

    clear_cache_pattern(ALL_STUDENT_DASHBOARD)

def clear_dashboard_cache(company_id=None, student_id=None, all_companies=False, all_students=False):

    clear_admin_dashboard_cache()

    if company_id is not None:
        clear_company_dashboard_cache(company_id)

    if student_id is not None:
        clear_student_dashboard_cache(student_id)

    if all_companies:
        clear_all_company_dashboard_cache()

    if all_students:
        clear_all_student_dashboard_cache()

# Error Definitions
 
class ValidationError(Exception):
    pass

class AuthenticationError(Exception):
    pass

class AuthorizationError(Exception):
    pass

class NotFoundError(Exception):
    pass

class ConflictError(Exception):
    pass

class ConversionError(Exception):
    pass

# Error Functions

def register_error_handlers(api):

    @api.errorhandler(ValidationError)
    def validation_error(error):
        return {"message": str(error)}, 400

    @api.errorhandler(AuthenticationError)
    def authentication_error(error):
        return {"message": str(error)}, 401

    @api.errorhandler(AuthorizationError)
    def authorization_error(error):
        return {"message": str(error)}, 403

    @api.errorhandler(NotFoundError)
    def not_found_error(error):
        return {"message": str(error)}, 404

    @api.errorhandler(ConflictError)
    def conflict_error(error):
        return {"message": str(error)}, 409

    @api.errorhandler(ConversionError)
    def conversion_error(error):
        return {"message": str(error)}, 422

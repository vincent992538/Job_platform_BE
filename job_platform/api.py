from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()

api.register_controllers(NinjaJWTDefaultController)

api.add_router("/jobs/", router="jobs.api.router", tags=["Jobs"])


@api.exception_handler(exc_class=ValidationError)
def django_validation_error_handler(
    request: HttpRequest, exception: ValidationError
) -> HttpResponse:
    """
    handel Django ValidationError
    """
    return api.create_response(
        request, {'detail': exception.message}, status=400
    )

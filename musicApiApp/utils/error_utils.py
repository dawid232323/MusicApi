from django.http import JsonResponse
from rest_framework import status


def get_error_response(error_message=None, response_status=None) -> JsonResponse:
    if error_message is None:
        error_message = 'Error occured please try again'
    if response_status is None:
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    return JsonResponse({'error_message': error_message}, status=response_status)
from django.http import JsonResponse
import os

class ResponseHandler:
    HTTP_STATUS_CODES = {
        'SUCCESS': {
            'code': 200,
            'success': True,
            'message': 'Success'
        },
        'NOT_FOUND': {
            'code': 404,
            'success': False,
            'message': 'The requested resource was not found'
        },
        'FORBIDDEN': {
            'code': 403,
            'success': False,
            'message': 'Permission denied'
        },
        'INTERNAL_SERVER_ERROR': {
            'code': 500,
            'success': False,
            'message': 'An error occurred while processing the request'
        },
        'VALIDATION_ERROR': {
            'code': 417,
            'success': False,
            'message': 'There was a validation error'
        },
        'UNAUTHORIZED': {
            'code': 401,
            'success': False,
            'message': 'Unauthorized'
        },
        'CONFLICT': {
            'code': 409,
            'success': False,
            'message': 'Conflict'
        }
    }

    @staticmethod
    def response(status_key, result=None, message=None, system_code=None):
        try:
            # Get status details
            http_status = ResponseHandler.HTTP_STATUS_CODES.get(status_key, ResponseHandler.HTTP_STATUS_CODES['INTERNAL_SERVER_ERROR'])
            
            # Set message
            if http_status['code'] == 500:
                debug_mode = os.getenv('APP_DEBUG', 'False').lower() in ['true', '1']
                final_message = message if debug_mode else http_status['message']
            else:
                final_message = message if message else http_status['message']
            
            # Return JSON response
            return JsonResponse({
                'is_success': http_status['success'],
                'message': final_message,
                'result': result,
                'system_code': system_code or '',
            }, status=http_status['code'])
        
        except Exception as e:
            return JsonResponse({
                'message': 'Please check the response service',
                'result': str(e),
            }, status=500)
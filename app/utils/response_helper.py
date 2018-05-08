from flask import jsonify, make_response


def success(data=None, message=None):
    """
    Success response
    :param message: success message
    :param data: response data
    :return: response
    """
    response = {'status': 'success'}
    if message:
        response['message'] = message
    if data:
        response['data'] = data
    return make_response(jsonify(response), 200)


def error(status_code=400, message='400 Bad Request', data=None):
    """
    Error response
    :param message: error message
    :param data: return some data when encounter errors, such as 422 error
    :param status_code: response status code
    :return: response
    """
    response = {'status': 'error', 'message': message}
    if data:
        response['data'] = data
    return make_response(jsonify(response), status_code)


def bad_request(message, data=None):
    return error(message=message, data=data) if data is not None else error(message=message, data=data)


def unauthorized(message):
    return error(status_code=401, message='401 Unauthorized')


def forbidden(message):
    return error(status_code=403, message='403 Forbidden')


def not_found(message):
    return error(status_code=404, message='404 Not Found')


def unprocessable_entity(message='422 Unprocessable Entity', data=None):
    return error(
        status_code=422,
        message=message,
        data=data
    )


def internal_error():
    return error(status_code=500, message='500 Internal Server Error')

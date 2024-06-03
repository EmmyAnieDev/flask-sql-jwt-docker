from flask import jsonify


def handle_401_error(e):
    return jsonify({'message': 'Unauthorized: Access is denied due to invalid credentials'}), 401


def handle_403_error(e):
    return jsonify({'message': 'Forbidden: You don’t have permission to access this resource'}), 403


def handle_404_error(e):
    return jsonify({'message': 'Not Found: Please check and confirm your request'}), 404


def handle_405_error(e):
    return jsonify({'message': 'Method Not Allowed: The method is not allowed for the requested URL'}), 405


def handle_500_error(e):
    return jsonify({'message': 'Internal Server Error, could not retrieve data'}), 500


def handle_400_error(e):
    return jsonify({'message': 'Bad Request: The server could not understand the request due to invalid syntax'}), 400


def handle_409_error(e):
    return jsonify({'message': 'Conflict: The request could not be completed due to a conflict with the current state of the resource'}), 409


def handle_429_error(e):
    return jsonify({'message': 'Too Many Requests: You have sent too many requests in a given amount of time'}), 429
def additional_logging_middleware(get_response):
    def middleware(request):
        if hasattr(request, "graylog"):
            if hasattr(request, "user"):
                request.graylog["user_id"] = str(request.user.id)
                request.graylog["user_username"] = request.user.username

            request.graylog["some_custom_field"] = "some_custom_value"
        response = get_response(request)
        return response

    return middleware

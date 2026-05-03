from .models import UserToken

class BlockBlacklistedAccessToken:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")

        if auth_header and " " in auth_header:
            token = auth_header.split(" ")[1]

            exists = UserToken.objects.filter(access_token=token).exists()

            if not exists:
                from django.http import JsonResponse
                return JsonResponse({"error": "Token expired or logged out"}, status=401)

        return self.get_response(request)
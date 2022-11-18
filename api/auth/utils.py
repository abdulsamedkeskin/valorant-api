def parse_accessToken(response):
    return response['response']['parameters']['uri'].split("&")[0].split("=")[1]
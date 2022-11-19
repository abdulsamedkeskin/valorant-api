def parse_accessToken(response):
    id_token = response['response']['parameters']['uri'].split("id_token=")[1].split("&")[0]
    access_token = response['response']['parameters']['uri'].split("&")[0].split("=")[1]
    return id_token, access_token
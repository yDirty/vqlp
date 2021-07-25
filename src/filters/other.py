import typing as ty
import re
import requests


def check_access_token(site: ty.Optional[str]) -> ty.Optional[dict]:
    if "access_token=" in site:
        site = re.findall(
            "access_token=[A-Za-z0-9]*",
            site
        )[0].replace("access_token=", "")

    regular_return = re.sub('[^A-Za-z0-9]', '', site) == site and len(
        site) == 85
    if not regular_return:
        return {"response": False, "desc": "Введите правильный формат токена."}

    json_response = requests.get("https://api.vk.com/method/users.get",
                                 params={
                                     "access_token": site,
                                     "v": 5.131
                                 }).json()

    try:
        _ = json_response['response']
        return {"response": True, "user": json_response, 'token': site}
    except:
        return {"response": False, "desc": "[5] Invalid token", "error": json_response}

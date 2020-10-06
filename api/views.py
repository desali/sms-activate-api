import time

from django.http import HttpResponse
import requests

from api.models import Number


def get_api_key():
    return '1807efA991Ac171785ccdcdf04d5602d'


def get_number(request):
    # Get Number
    api_key = get_api_key()
    service = 'ig'
    country = 0
    resp = requests.get("https://sms-activate.ru/stubs/handler_api.php?api_key={}&action=getNumber&service={}"
                        "&country={}".format(api_key, service, country))

    if resp.text == "NO_NUMBERS":
        country = 2
        resp = requests.get("https://sms-activate.ru/stubs/handler_api.php?api_key={}&action=getNumber&service={}"
                            "&country={}".format(api_key, service, country))

    if ':' not in resp.text:
        return HttpResponse(resp.text)

    number_id = resp.text.split(':')[1]
    number_number = resp.text.split(':')[2]

    number = Number(operation_id=number_id, number=number_number)
    number.save()

    return HttpResponse(number.number)


def number_status(request):
    # Change status
    number_number = request.GET['number']
    status = request.GET['status']

    number = Number.objects.get(number=number_number)
    api_key = get_api_key()

    if status == '1':
        resp = requests.get("https://sms-activate.ru/stubs/handler_api.php?api_key={}&action=setStatus&status={}&id={}"
                            "".format(api_key, 1, number.operation_id))

        return HttpResponse(resp.text)
    elif status == '2':
        while True:
            resp = requests.get("https://sms-activate.ru/stubs/handler_api.php?api_key={}&action=getStatus&id={}"
                                "".format(api_key, number.operation_id))

            if "STATUS_OK" in resp.text:
                return HttpResponse(resp.text.split(':')[1])
            time.sleep(10)
    elif status == '3':
        resp = requests.get("https://sms-activate.ru/stubs/handler_api.php?api_key={}&action=setStatus&status={}&id={}"
                            "".format(api_key, 3, number.operation_id))

        return HttpResponse(resp.text)
    elif status == '4':
        resp = requests.get("https://sms-activate.ru/stubs/handler_api.php?api_key={}&action=setStatus&status={}&id={}"
                            "".format(api_key, 6, number.operation_id))

        number.delete()
        return HttpResponse(resp.text)

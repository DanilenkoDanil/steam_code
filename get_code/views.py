from django.shortcuts import render
from django.http import HttpResponse
from get_code.models import Key, Shop, SteamCode, PurchaseType
from get_code.api import check_code


def get_shops():
    return Shop.objects.all()


def get_key(key: str):
    try:
        return Key.objects.filter(key=key)[0]
    except IndexError:
        return False


def get_purchase_type(amount: float):
    try:
        return PurchaseType.objects.filter(amount=amount)[0]
    except IndexError:
        return False


def get_code_list(str_list: str) -> list:
    final_list = []
    str_list = str_list.split(', ')
    print(str_list)
    for code in str_list:
        final_list.append(int(code))
    return final_list


# Поправь amount
def index(request):
    code = request.GET.get('uniquecode')
    key = get_key(code)
    if key is False:
        for shop in get_shops():
            # info = check_code(code, shop.guid, shop.seller_id)
            amount = get_purchase_type(500)
            codes_list = get_code_list(amount.codes_list)
            if True:
                final_code_str = "| "
                key = Key.objects.create(key=code, amount=500)
                for code_value in codes_list:
                    steam_code = SteamCode.objects.get(status=True, value=code_value)
                    print('1')
                    steam_code.status = False
                    steam_code.key = key
                    steam_code.save()
                    final_code_str += str(steam_code.code) + " | "

                return render(
                    request,
                    'get_code/account.html',
                    {
                        'key': code,
                        'code': final_code_str,
                        'amount': key.amount
                    }
                )
            else:
                continue

        html = f"Код {code} не действителен!"
        return HttpResponse(html)
    else:
        final_code_str = "| "
        for code in SteamCode.objects.filter(key=key):
            final_code_str += str(code.code) + " | "
        return render(
            request,
            'get_code/account.html',
            {
                'key': key.key,
                'code': final_code_str,
                'amount': key.amount
            }
        )

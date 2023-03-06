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
    uniquecode = request.GET.get('uniquecode')
    key = get_key(uniquecode)
    if key is False:
        for shop in get_shops():
            info = check_code(uniquecode, shop.guid, shop.seller_id)
            print(info)
            print(info['options'])
            amount_num = int(info['options'][0]['value'].split()[0])
            amount = get_purchase_type(amount_num)
            if amount is False:
                final_code_str = "Произошла ошибка! Обратитесь к продавцу"
                return render(
                    request,
                    'get_code/account.html',
                    {
                        'key': uniquecode,
                        'code': final_code_str,
                        'amount': amount_num
                    }
                )
            print(amount)
            codes_list = get_code_list(amount.codes_list)
            if info['retval'] == 0:
                final_code_str = "| "
                steam_code_list = []
                for code_value in codes_list:
                    current_code = SteamCode.objects.filter(status=True, value=code_value).last()
                    if current_code is not None:
                        current_code.status = False
                        current_code.save()
                        steam_code_list.append(current_code)
                    else:
                        for code in steam_code_list:
                            code.status = True
                            code.save()
                        final_code_str = "Произошла ошибка! Обратитесь к продавцу"
                        return render(
                            request,
                            'get_code/account.html',
                            {
                                'key': uniquecode,
                                'code': final_code_str,
                                'amount': amount_num
                            }
                        )
                key = Key.objects.create(key=uniquecode, amount=amount_num)
                for steam_code in steam_code_list:
                    steam_code.key = key
                    steam_code.save()
                    final_code_str += str(steam_code.code) + " | "

                return render(
                    request,
                    'get_code/account.html',
                    {
                        'key': uniquecode,
                        'code': final_code_str,
                        'amount': key.amount
                    }
                )
            else:
                continue

        html = f"Код {uniquecode} не действителен!"
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

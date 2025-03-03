import json

import requests


def get_usd_exchange_rate(api_key1, base_currency="USD", target_currency="RUB"):
    """Функция обмена валюты по курсу"""
    path = "https://api.apilayer.com/currency_data/live"
    headers = {"apikey": api_key}
    params = {"currencies": target_currency, "source": base_currency}
    try:
        response = requests.get(path, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data and data.get("success"):
            rates = data.get("quotes")
            if rates:
                rate_key = f"{base_currency}{target_currency}"
                exchange_rate = rates.get(rate_key)
                if exchange_rate:
                    return exchange_rate
                else:
                    print(f"Ошибка: Не удалось найти курс для {rate_key} в ответе API.")
                    return None
            else:
                print("Ошибка: Ключ 'quotes' не найден в ответе API.")
                return None
        else:
            print(f"Ошибка: Не удалось получить курс обмена. Ответ API: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса API: {e}")
        return None
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат ответа API (ожидался JSON).")
        return None


if __name__ == "__main__":
    api_key = "tP6pidXH3QMCPZmCOPfsyXE8CQxsvxMk"
    exchange_rate = get_usd_exchange_rate(api_key)

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests, random


def weather(request):
    city = request.GET.get("city", "Hyderabad")
    api_key = settings.OPENWEATHER_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return JsonResponse({"error": "City not found"}, status=400)

        result = {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"].capitalize(),
        }
        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def convert(request):
    amount = request.GET.get("amount")
    to_currency = request.GET.get("to", "USD").upper()

    if not amount or not amount.replace(".", "", 1).isdigit():
        return JsonResponse({"error": "Invalid amount"}, status=400)

    amount = float(amount)

    api_key = settings.EXCHANGERATE_KEY
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/INR"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("result") != "success":
            return JsonResponse({"error": "Failed to fetch currency data"}, status=400)

        rate = data["conversion_rates"].get(to_currency)
        if not rate:
            return JsonResponse(
                {"error": f"Unsupported currency '{to_currency}'"}, status=400
            )

        converted = round(amount * rate, 2)
        return JsonResponse(
            {
                "amount_in_inr": amount,
                "to": to_currency,
                "converted_amount": converted,
                "rate": rate,
            }
        )

    except Exception as e:
        return JsonResponse({"error": f"Internal error: {e}"}, status=500)


def quote(request):
    api_key = settings.QUOTES_API_KEY
    url = "https://api.api-ninjas.com/v1/quotes?category=inspirational"

    try:
        response = requests.get(url, headers={"X-Api-Key": api_key})
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            return JsonResponse(
                {"quote": data[0]["quote"], "author": data[0]["author"]}
            )

        return JsonResponse(
            {
                "quote": "Believe in yourself and you’re halfway there.",
                "author": "Theodore Roosevelt",
                "source": "fallback",
            }
        )

    except Exception as e:
        fallback_quotes = [
            {"quote": "Success is no accident.", "author": "Pele"},
            {
                "quote": "The harder you work, the luckier you get.",
                "author": "Gary Player",
            },
            {"quote": "Dream big, start small, act now.", "author": "Robin Sharma"},
        ]
        return JsonResponse(random.choice(fallback_quotes))


def home(request):
    return render(request, "index.html")

import requests

from .models import CurrencyModel

from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Max


class CurrentView(View):
    def get(self, request):
        last_10_records = CurrencyModel.objects.all()[:10]

        if last_10_records:
            last_datetime = last_10_records[0].datetime
            current_datetime = timezone.now()

            if (current_datetime - last_datetime).total_seconds() > 10:
                url = "http://apilayer.net/api/live?access_key=89696ec611480d51b74c31ce00f2951f"
                response = requests.get(url)
                data = response.json()
                value = data['quotes']['USDRUB']

                CurrencyModel.objects.create(price=value)

                last_10_records = CurrencyModel.objects.all()[:10]             

        else:
            url = "http://apilayer.net/api/live?access_key=89696ec611480d51b74c31ce00f2951f"
            response = requests.get(url)
            data = response.json()
            value = data['quotes']['USDRUB']
            
            CurrencyModel.objects.create(price=value)
            last_10_records = CurrencyModel.objects.all()[:10]
        
        return JsonResponse({
            'price': value,
            'last_10_records': [
                {'datetime': req.datetime.strftime('%Y-%m-%d %H:%M:%S'), 'price': req.price}
                for req in last_10_records
            ]
        })
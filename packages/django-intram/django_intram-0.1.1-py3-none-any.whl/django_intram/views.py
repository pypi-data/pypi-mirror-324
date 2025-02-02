from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .intram import Intram
import json

@csrf_exempt
def initialize_payment(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        intram = Intram(
            public_key=settings.INTRAM_PUBLIC_KEY,
            private_key=settings.INTRAM_PRIVATE_KEY,
            secret=settings.INTRAM_SECRET,
            marchand_id=settings.INTRAM_MARCHAND_ID,
            sandbox=getattr(settings, 'INTRAM_SANDBOX', False)
        )
        
        # Configure payment details
        intram.set_currency(data.get('currency', 'XOF'))
        intram.set_amount(data['amount'])
        intram.set_items(data.get('items', []))
        intram.set_description(data.get('description', ''))
        intram.set_name_store(data.get('store_name', ''))
        intram.set_template(data.get('template', 'default'))
        
        # Set URLs
        base_url = request.build_absolute_uri('/')[:-1]
        intram.set_return_url(data.get('return_url', f'{base_url}/payment/success/'))
        intram.set_cancel_url(data.get('cancel_url', f'{base_url}/payment/cancel/'))
        intram.set_redirection_url(f'{base_url}/django-intram/payment/callback/')
        
        # Initialize payment
        response = intram.set_request_payment()
        return JsonResponse(response)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def payment_callback(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        # Process callback data
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def payment_status(request, transaction_id):
    try:
        intram = Intram(
            public_key=settings.INTRAM_PUBLIC_KEY,
            private_key=settings.INTRAM_PRIVATE_KEY,
            secret=settings.INTRAM_SECRET,
            marchand_id=settings.INTRAM_MARCHAND_ID,
            sandbox=getattr(settings, 'INTRAM_SANDBOX', False)
        )
        
        status = intram.get_transaction_status(transaction_id)
        return JsonResponse(status)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

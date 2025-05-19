# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import TestModel
import threading
from django.db import transaction

# 1. Signal execution (sync)
def signal_sync_view(request):
    import time
    from django.db.models.signals import post_save

    start = time.time()
    TestModel.objects.create(name="test")
    end = time.time()
    return JsonResponse({
        "question": "Are Django signals executed synchronously or asynchronously?",
        "answer": "Django signals are executed synchronously by default.",
        "message": "Signal triggered",
        "time_taken_seconds": round(end - start, 2)
    })

# 2. Signal thread test
def signal_thread_view(request):
    main_thread = threading.get_ident()
    TestModel.objects.create(name="thread_test")
    return JsonResponse({
        "question": "Do Django signals run in the same thread as the caller?",
        "answer": "Yes, by default Django signals run in the same thread.",
        "main_thread_id": main_thread,
        "note": "Signal handler prints thread ID"
    })

# 3. Signal transaction test
def signal_transaction_view(request):
    try:
        with transaction.atomic():
            TestModel.objects.create(name="raise")  # raises from signal
    except Exception as e:
        rolled_back = not TestModel.objects.filter(name="raise").exists()
        return JsonResponse({
             "question": "Do Django signals run in the same database transaction as the caller?",
            "answer": "Yes, by default Django signals run in the same DB transaction as the caller.",
            "exception": str(e),
            "rolled_back": rolled_back
        })
    return JsonResponse({
        "question": "Do Django signals run in the same database transaction as the caller?",
        "answer": "Yes, by default Django signals run in the same DB transaction as the caller.",
        "status": "should not reach here"
        })

# 4. Custom iterable class
class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}

def rectangle_view(request):
    rect = Rectangle(10, 5)
    data = [i for i in rect]
    return JsonResponse({
        "question": "How can we make a custom class iterable in Python?",
        "answer": "By defining the __iter__() method and yielding desired values. Here, length and width are yielded one after the other.",
        "rectangle": data
        })

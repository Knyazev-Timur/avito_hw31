import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Category, Ad


def index(request):
    return JsonResponse({"Status": "server is UP"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CatView(View):

    def get(self, request):
        get_all = Category.objects.all()
        return JsonResponse([{"id": category.id, "name": category.name} for category in get_all], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_category = Category.objects.create(**data)
        print(new_category)
        return JsonResponse({"id": new_category.id, "name": new_category.name})


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):

    def get(self, request):
        get_all = Ad.objects.all()
        return JsonResponse([{
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published}
            for ad in get_all], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        ad = Ad.objects.create(**data)
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published})


class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({"id": category.id, "name": category.name})


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({
            'id': ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published})

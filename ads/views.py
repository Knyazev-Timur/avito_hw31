import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad
from avito_hw27.settings import TOTAL_ON_PAGE
from user.models import User


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
        return JsonResponse({"id": new_category.id, "name": new_category.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Category
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        new_category = Category.objects.create(name=data.get("name"))

        return JsonResponse({"id": new_category.id, "name": new_category.name})

@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = "__all__"
    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data.get("name")
        self.object.save()
        return JsonResponse({"id": self.object.id, "name": self.object.name})

@method_decorator(csrf_exempt, name='dispatch')
class CatDelView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        cat = self.get_object()
        super().delete(request, *args, **kwargs)
        return JsonResponse({"delete ID": cat.id})


class CatListView(ListView):
    model = Category
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse([{"id": category.id, "name": category.name} for category in self.object_list.order_by("name")], safe=False)


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
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "address": [loc.name for loc in ad.author.location.all()],
            "is_published": ad.is_published,
            "category": ad.category.name})

class AdListView(ListView):
    model = Ad
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("-price")
        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get("page", 1)
        page_object = paginator.get_page(page_number)
        return JsonResponse({"total": page_object.paginator.count,
                             "num_pages": page_object.paginator.num_pages,
                             "items": [{
                                        'id': ad.id,
                                        "name": ad.name,
                                        "author": ad.author.username,
                                        "price": ad.price,
                                        "description": ad.description,
                                        "address": [loc.name for loc in ad.author.location.all()],
                                        "is_published": ad.is_published,
                                        "category": ad.category.name,
                                        "image": ad.image.url
                             } for ad in page_object]}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        author = get_object_or_404(User, pk=data["author_id"])
        category = get_object_or_404(Category, pk=data.pop("category_id"))
        ad = Ad.objects.create(author=author, category=category, **data)

        return JsonResponse({
            'id': ad.id,
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "address": [loc.name for loc in ad.author.location.all()],
            "is_published": ad.is_published,
            "category": ad.category.name})


@method_decorator(csrf_exempt, name='dispatch')
class AdDelView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        ad = self.get_object()
        super().delete(request, *args, **kwargs)
        return JsonResponse({"delete ID": ad.id})


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = "__all__"
    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if "name" in data:
            self.object.name =data.get("name")
        if "author_id" in data:
            author = get_object_or_404(User, pk=data.get("author_id"))
            self.object.author = author
        if "price" in data:
            self.object.price =data.get("price")
        if "description" in data:
            self.object.description =data.get("description")
        if "is_published" in data:
            self.object.is_published =data.get("is_published")
        ad = self.object
        ad.save()
        # self.object.save()
        return JsonResponse({
            'id': ad.id,
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "address": [loc.name for loc in ad.author.location.all()],
            "is_published": ad.is_published,
            "category": ad.category.name})


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImg(UpdateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'image': self.object.image.url})

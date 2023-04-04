import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, Selection
from ads.permissions import IsOwner, IsStaff
from ads.serializers import AdSerializer, AdListSerializer, AdDetailSerializer, SelectionSerializer, \
    SelectionListSerializer, SelectionCreateSerializer, SelectionDetailSerializer


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


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by("-price")
    default_serializer_class = AdSerializer
    default_permission = [AllowAny]


    permission = {
        "retrieve": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner | IsStaff],
        "partial_update": [IsAuthenticated, IsOwner | IsStaff],
        "destroy": [IsAuthenticated, IsOwner | IsStaff],
    }

    serializers = {
        "list": AdListSerializer,
        "retrieve": AdDetailSerializer,
        "create": AdListSerializer
    }
    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permission.get(self.action, self.default_permission)]

    def list(self, request, *args, **kwargs):
        cat = request.GET.getlist("cat", [])
        if cat:
            self.queryset = self.queryset.filter(category_id__in=cat)

        text = request.GET.get("text")
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location")
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get("price_from")
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get("price_to")
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.order_by("name")
    default_serializer_class = SelectionSerializer
    default_permission = [AllowAny]
    permission = {
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner],
        "partial_update": [IsAuthenticated, IsOwner],
        "destroy": [IsAuthenticated, IsOwner],
    }
    serializers = {
        "list": SelectionListSerializer,
        "create": SelectionCreateSerializer,
        "retrieve": SelectionDetailSerializer
    }
    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permission.get(self.action, self.default_permission)]

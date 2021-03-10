from rest_framework import viewsets
# importamos modelo de listelement - Element, Category, Type
from .models import Element, Category, Type
# importamos serializer con los modelos Element, Category y Type
from .serializer import ElementSerializer, CategorySerializer, TypeSerializer , CommentSerializer
# para los ejemplos del profe
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# importamos modelo comment
from comment.models import Comment

#acciones extras de rest framework
from rest_framework.decorators import action

class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer

    @action(detail=False, methods=['get'])
    def all(self, request):
        # este objects.all() nos enviará todos los registros, da igual el id que coloquemos en el url
        # queryset = Element.objects.all()
        # si queremos filtrar cada url perteneciente a su elemento
        queryset = Element.objects.all()
        serializer = ElementSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def url(self, request):
        #queryset = Element.objects.get(url_clean=request.query_params['url_clean'])
        queryset = get_object_or_404(Element,url_clean=request.query_params['url_clean'])
        serializer = ElementSerializer(queryset, many=False)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def elements(self, request, pk=None):
        # este objects.all() nos enviará todos los registros, da igual el id que coloquemos en el url
        # queryset = Element.objects.all()
        # si queremos filtrar cada url perteneciente a su elemento
        queryset = Element.objects.filter(category_id=pk)
        serializer = ElementSerializer(queryset, many=True)
        return Response(serializer.data)

    #para listar todo sin paginar
    @action(detail=False, methods=['get'])
    def all(self, request):
        # este objects.all() nos enviará todos los registros, da igual el id que coloquemos en el url
        # queryset = Element.objects.all()
        # si queremos filtrar cada url perteneciente a su elemento
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def url(self, request):
        queryset = get_object_or_404(Category,url_clean=request.query_params['url_clean'])
        serializer = CategorySerializer(queryset, many=False)
        return Response(serializer.data)

    #sacado de doc django rest
    '''def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)'''

# si queremos limitar, en caso que solo puedan tener el GET en lugar de DELETE O PUT, usamos ReadOnlyModelViewSet
class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    @action(detail=True, methods=['get'])
    def elements(self, request, pk=None):
        # este objects.all() nos enviará todos los registros, da igual el id que coloquemos en el url
        # queryset = Element.objects.all()
        # si queremos filtrar cada url perteneciente a su elemento
        queryset = Element.objects.filter(type_id=pk)
        serializer = ElementSerializer(queryset, many=True)
        return Response(serializer.data)

    #para listar todo sin paginar
    @action(detail=False, methods=['get'])
    def all(self, request):
        # este objects.all() nos enviará todos los registros, da igual el id que coloquemos en el url
        # queryset = Element.objects.all()
        # si queremos filtrar cada url perteneciente a su elemento
        queryset = Type.objects.all()
        serializer = TypeSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def url(self, request):
        queryset = get_object_or_404(Type,url_clean=request.query_params['url_clean'])
        serializer = TypeSerializer(queryset, many=False)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    # excluir comentarios que no tienen elementos
    queryset = Comment.objects.exclude(element__isnull=True)
    serializer_class = CommentSerializer

    #para listar todo sin paginar
    @action(detail=False, methods=['get'])
    def all(self, request):
        # este objects.all() nos enviará todos los registros, da igual el id que coloquemos en el url
        # queryset = Element.objects.all()
        # si queremos filtrar cada url perteneciente a su elemento
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

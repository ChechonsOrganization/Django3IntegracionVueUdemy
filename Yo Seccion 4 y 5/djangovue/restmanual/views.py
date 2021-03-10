from django.shortcuts import render
# importar api de django y no de restframework, y http response 
from django.http import JsonResponse, HttpResponse
# importar rest_framework.response para indicar una clase con la cual podremos emplear una respuesta valida
from rest_framework.response import Response
# aplicar decoradores api_view
from rest_framework.decorators import api_view
# importar rest_framework status
from rest_framework import status
# importar listelement modelos y serializadores
from listelement.models import Element, Type
from listelement.serializer import ElementSerializer, ElementSerializerSimple
# importar api view para la clases
from rest_framework.views import APIView
# importar mixins de rest framework y generic api view
from rest_framework import mixins, generics
# crear paginacion personalizada para los json en rest_framework
from rest_framework.pagination import PageNumberPagination
# importar la autenticacion del rest
from rest_framework.authentication import BasicAuthentication
# importar permisos para consumir el rest api
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

# Create your views here.

# no siempre es necesario crear una rest api, quizas queramos pocos metodos,
# donde solo queremos obtener unos pocos datos para consumir en algun framework front

# Crear funcion manualJson, devuelve un JSON estático
def manualJson(request):

    # data (diccionario) estatica o que venga fuera de una bbdd
    data = {
        'id': 123,
        'name': 'Pepe'
    }

    #return JsonResponse(data)

    # trabajar cond data de BD
    # la data en este punto el JsonResponse no puede trabajar con los 
    # Elementos asi en la variable data, se necesita convertir el formato a json
    # para que funcione, para eso creamos response para serializar nuestros datos
    data = Element.objects.all()
    response = {'elements': list(data.values('id','title', 'description'))}

    return JsonResponse(response)

# creamos una clase para la paginacion personalizada
class ProductPagination(PageNumberPagination):
    page_size = 2 
    # creamos funcion para pa personalizar el paginado
    def get_paginated_response(self, data):
        return Response({
            'enlaces': {
                'siguiente': self.get_next_link(),
                'previo': self.get_previous_link()
            },
            'contados': self.page.paginator.count,
            'resultados': data
        })

# clases genericas para crud pero mas reducidas en codigo
class ProductList(generics.ListCreateAPIView):
    # obtener todos los listados que sean tipo producto
    type = Type.objects.get(pk=2) # tipo producto
    # creamos queryset para listar los elementos por el tipo
    queryset = Element.objects.filter(type=type)
    # serializamos
    serializer_class = ElementSerializerSimple
    # seteamos la paginacion personalizada, llamando a la clase ProductPagination
    pagination_class = ProductPagination
    # variable para autorizar al usuario loggeado para ver el rest api
    authentication_classes = [BasicAuthentication]
    # permisos para consumir la rest api
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    # obtener todos los listados que sean tipo producto
    type = Type.objects.get(pk=2) # tipo producto
    # creamos queryset para listar los elementos por el tipo
    queryset = Element.objects.filter(type=type)
    # serializamos
    serializer_class = ElementSerializerSimple

# crear clase que herede el mixin para hacer operaciones crud sin repetir tanto codigo
"""
class ProductList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    # obtener todos los listados que sean tipo producto
    type = Type.objects.get(pk=2) # tipo producto
    queryset = Element.objects.filter(type=type)
    serializer_class = ElementSerializerSimple

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
"""

# crear clase que herede el mixin para el get, put y delete generico
"""
class ProductDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    # obtener todos los listados que sean tipo producto
    type = Type.objects.get(pk=2) # tipo producto
    queryset = Element.objects.filter(type=type)
    serializer_class = ElementSerializerSimple

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request,pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)
"""


# Haremos esto pero a traves de clases
# APIView es lo mismo que el decorador de @api_view
# asi la clase se usa para los metodos http
"""class ProductList(APIView):

    def get(self, request):
        # obtener todos los listados que sean tipo producto
        type = Type.objects.get(pk=2) # tipo producto
        products = Element.objects.filter(type=type)
        # variable para serialziar los productos
        serializers = ElementSerializer(products, many=True) # forma en cual le pasamos mas de un objeto al json
        # devolvemos la respuesta
        return Response(serializers.data)

    def post(self, request):
        serializer = ElementSerializerSimple(data=request.data)
        # preguntar si la data es valida
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

"""
class ProductDetail(APIView):
    def get_object(self, pk):
        # obtener todos los listados que sean tipo producto
        type = Type.objects.get(pk=2) # tipo producto
        product = Element.objects.get(type=type,pk=pk)
        return product

    def get(self, request, pk):
        # buscar el producto
        product = self.get_object(pk)
        # variable para serialziar los productos
        serializers = ElementSerializer(product) # forma en cual le pasamos mas de un objeto al json
        # devolvemos la respuesta
        return Response(serializers.data)

    def put(self, request, pk):
        # buscar producto
        product = self.get_object(pk)
        # variable para serialziar los productos
        serializer = ElementSerializerSimple(product, data=request.data)
        # preguntar si la data es valida
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # buscar producto
        product = self.get_object(pk)
        # borrar producto
        product.delete()
        # enviar respuesta
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

# crear otra lista json manual
@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        # obtener todos los listados que sean tipo producto
        type = Type.objects.get(pk=2) # tipo producto
        products = Element.objects.filter(type=type)
        # variable para serialziar los productos
        serializers = ElementSerializer(products, many=True) # forma en cual le pasamos mas de un objeto al json
        # devolvemos la respuesta
        return Response(serializers.data)

    if request.method == 'POST':
        serializer = ElementSerializerSimple(data=request.data)
        # preguntar si la data es valida
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# funcion para obtener, actualizar y borrar los productos colocando su id
@api_view(['GET','PUT','DELETE'])
def product_detail(request, pk):
    
    # obtener todos los listados que sean tipo producto
    type = Type.objects.get(pk=2) # tipo producto
    product = Element.objects.get(type=type,pk=pk)
    
    if request.method == 'GET':
        # variable para serialziar los productos
        serializers = ElementSerializer(product) # forma en cual le pasamos mas de un objeto al json
        # devolvemos la respuesta
        return Response(serializers.data)
    elif request.method == 'PUT':
        serializer = ElementSerializerSimple(product, data=request.data)
        # preguntar si la data es valida
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
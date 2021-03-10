from rest_framework import serializers
# importar modelo de listelement - Element, Category y Type
from .models import Element, Category, Type
# importar modelo comment
from comment.models import Comment

# generamos esta app para ser consumida por una API

class CommentSerializer(serializers.ModelSerializer):
    
    count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        # podemos mostrar uno, varios o todos
        #fields = ['text']
        fields = '__all__'

    def get_count(self, obj):
        
        print(obj)
        
        return Comment.objects.filter(element_id = obj.element_id).count()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class ElementSerializer(serializers.ModelSerializer):
    # aquí busca el __str__ de cada relación, o sea debe ser el mismo nombre
    category = CategorySerializer(read_only=True) #serializers.StringRelatedField()
    type = TypeSerializer(read_only=True)#serializers.StringRelatedField()
    # y para capturar los elementos que se relacionen en comments
    comments = CommentSerializer(read_only=True, many=True) #serializers.StringRelatedField(many=True)

    class Meta:
        model = Element
        fields = '__all__'


# Serializer que utilizaremos en la app restmanual para crear elementos por POST
class ElementSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'
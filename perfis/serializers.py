from rest_framework import serializers, exceptions, status
from .models import Perfil, Convite
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User


class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ('id', 'nome', 'email')

class PerfilSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField()
    contatos = ContatoSerializer(required=False, many=True)

    class Meta:
        model = Perfil
        fields = ('id', 'nome', 'email', 'nome_empresa', 'senha', 'contatos')
        read_only_fields = ('id',)

    def create(self, validated_data):
        try:
            usuario = User(username=validated_data['nome'], email=validated_data['email'])
            usuario.set_password(validated_data['senha'])
            usuario.save()

        except:
            raise exceptions.ParseError('Já existe um usuário cadastrado com esse nome', code=status.HTTP_400_BAD_REQUEST)

        Token.objects.create(user=usuario)
        validated_data['usuario'] = usuario

        del validated_data['email']
        del validated_data['senha']

        return super().create(validated_data)


class PerfilSimplicadoSerializer(serializers.ModelSerializer):
    pode_convidar = serializers.SerializerMethodField()

    class Meta:
        model = Perfil
        fields = ('id', 'nome', 'email', 'pode_convidar')
        read_only_fields = ('id',)


    def get_pode_convidar(self, obj):
        user = self.context['request'].user
        contatos = user.perfil.contatos.all()
        perfil = obj
        perfil_logado = user.perfil

        if perfil not in contatos and perfil != perfil_logado:
            return True
        return False


class ConviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convite
        fields = ('id', 'convidado', 'solicitante')
        read_only_fields = ('id',)

# from rest_framework import serializers, exceptions, status
# from .models import Perfil, Convite

# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token

# class ContatoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Perfil
#         fields = ('id', 'nome', 'email')

# class PerfilSerializers(serializers.ModelSerializer):
#     senha = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
#     email = serializers.EmailField()
#     contatos = ContatoSerializer(required=False, many=True)

#     class Meta:
#         model = Perfil
#         fields = ('id', 'nome', 'email', 'nome_empresa', 'senha', 'contatos')
#         read_only_fields = ('id',)

#     def create(self, validated_data):
#         try:
#             usuario = User(username=validated_data['nome'], email=validated_data['email'])
#             usuario.set_password(validated_data['senha'])
#             usuario.save()
#         except:
#             raise exceptions.ParseError('Já existe um usuário cadastrado com esse nome',
#              code=status.HTTP_400_BAD_REQUEST)

#         Token.objects.create(user=usuario)
#         validated_data['usuario'] = usuario

#         del validated_data['email']
#         del validated_data['senha']

#         return super().create(validated_data)

# class PerfilSimplicadoSerializer(serializers.ModelSerializer):
#     pode_convidar = serializers.SerializerMethodField()

#     class Meta:
#         model: Perfil
#         field = ('id', 'nome', 'email', 'pode_convidar')
#         read_only_fields = ('id',)

#     def get_pode_convidar(self, obj):
#         user = self.context['request'].user
#         contatos = user.perfil.contatos.all()
#         perfil = obj
#         perfil_logado = user.perfil

#         if perfil not in contatos and perfil != perfil_logado:
#             return True
            
#         return False


# class ConviteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Convite
#         fields = ('id', 'convidado', 'solicitante')
#         read_only_fields = ('id',)
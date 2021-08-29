from django.shortcuts import render, redirect
from perfis.models import Perfil, Convite
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, response, status, exceptions
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.permissions import AllowAny

from .serializers import PerfilSerializer, PerfilSimplicadoSerializer, ConviteSerializer


class PerfilViewSet(viewsets.ModelViewSet):
	queryset = Perfil.objects.all()
	serializer_class = PerfilSerializer

	def get_serializer_class(self):
		if self.request.method == 'GET':
			return PerfilSimplicadoSerializer 
		return super().get_serializer_class()
	
	def get_permissions(self):
		if self.request.method == 'POST':
			return (AllowAny(),)
		return super().get_permissions()

@api_view(['GET'])
@renderer_classes((JSONRenderer, BrowsableAPIRenderer))
def get_convites(request, *args, **kwargs):
	perfil_logado = get_perfil_logado(request)
	convites = Convite.objects.filter(convidado=perfil_logado)
	serializer = ConviteSerializer(convites, many=True)
	return response.Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@renderer_classes((JSONRenderer, BrowsableAPIRenderer))
def convidar(request, *args, **kwargs):
	try: 
		perfil_a_convidar = Perfil.objects.get(id=kwargs['perfil_id'])
	except:
		raise exceptions.NotFound('Não foi encontrado um perfil com o id informado.')
	perfil_logado = get_perfil_logado(request)
	if perfil_a_convidar != perfil_logado:
		perfil_logado.convidar(perfil_a_convidar)
		return response.Response({
			'messagem': f'Convite enviado com sucesso para {perfil_a_convidar.email}.'},
			status=status.HTTP_201_CREATED)
	raise exceptions.ParseError('Você não pode convidar o perfil com o id informado.')

@api_view(['POST'])
@renderer_classes((JSONRenderer, BrowsableAPIRenderer))
def aceitar(request, *args, **kwargs):
	perfil_logado = get_perfil_logado(request)
	try:
		convite = Convite.objects.filter(convidado=perfil_logado).get(id=kwargs['convite_id'])
	except:
		raise exceptions.NotFound('Não foi encontrado um convite com o informado')
	convite.aceitar()
	return response.Response({'menssagem': 'Convite aceito com sucesso.'},
							  status=status.HTTP_201_CREATED)

@api_view(['GET'])
@renderer_classes((JSONRenderer, BrowsableAPIRenderer))
def get_meu_perfil(request, *args, **kwargs):
	perfil_logado = get_perfil_logado(request)
	serializer = PerfilSerializer(perfil_logado)
	return response.Response(serializer.data, status=status.HTTP_200_OK)

def get_perfil_logado(request):
	return request.user.perfil



# from django.http import response
# from django.shortcuts import render, redirect
# from rest_framework import serializers
# # from rest_framework.serializers import Serializer

# from perfis.models import Perfil, Convite
# from django.contrib.auth.decorators import login_required
# from rest_framework import viewsets, response, status, exceptions
# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
# from rest_framework.permissions import AllowAny

# from perfis.serializers import PerfilSerializer
# from .serializers import PerfilSimplicadoSerializer
# from .serializers import ConviteSerializer
# #End Point - realiza criação de novo perfil e retorna perfis cadastrados
# class PerfilViewSet(viewsets.ModelViewSet):
#    queryset = Perfil.objects.all()
#    serializer_class = PerfilSerializer

#    def get_serializer_class(self):
#        if self.request.method == 'GET':
# 		      return PerfilSimplicadoSerializer
#        return super().get_serializer_class()

#    def get_permissions(self):
#        if self.request.method == 'POST':
# 		      return (AllowAny(),)
#        return super().get_permissions()

# #implementação de decoradores dos EndPoints e Métodos/verbos GET e POST
# @api_view(['GET'])
# @renderer_classes((JSONRenderer, BrowsableAPIRenderer))
# def get_convites(request, *args, **kwargs):
# 	perfil_logado = get_perfil_logado(request)
# 	convites = Convite.objects.filter(convidado = perfil_logado)
# 	serializer = ConviteSerializer(convites, many=True)
# 	return response.Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# @renderer_classes((JSONRenderer, BrowsableAPIRenderer))
# def convidar(request, *args, **kwargs):	
# 	try: #para tratar o erro de perfil inexistente usar o try
# 		perfil_a_convidar = Perfil.objects.get(id=kwargs['perfil_id'])
# 	except:#Como não há relação entre Front e BackEnd pode ser passado um 
# 		#perfil não relacionado ao id, para tratar isso a aplicação retorna um erro que é exeção
# 		raise exceptions.NotFound('Não encontrado Perfil relacionado ao id informado')
# 	perfil_logado = get_perfil_logado(request)	
# 	if perfil_a_convidar != perfil_logado:
# 		perfil_logado.convidar(perfil_a_convidar)
# 		# f antes da string permite passar variáveis dentro da string
# 		return response.Response({
# 			'messagem': f'Convite enviado com sucesso para {perfil_a_convidar.email}.'},
# 			status=status.HTTP_201_CREATED)
# 	raise exceptions.ParseError('Não é possível convidar o perfil do id informado')		
	
# @api_view(['POST'])
# @renderer_classes((JSONRenderer, BrowsableAPIRenderer))
# def aceitar(request, *args, **kwargs):
# 	perfil_logado = get_perfil_logado(request)
# 	try:
# 		convite = Convite.objects.filter(convidado=perfil_logado).get(id=kwargs['convite_id'])
# 		#se o id enviado para aceitar o convite não estiver na lista exibida tratar a exceção
# 	except:
# 		raise exceptions.NotFound('Não foi encontrado um convite com o id informado. ')
# 	convite.aceitar()
# 	return response.Response({'Mensagem': 'Convite aceito com sucesso'}, 
# 			status=status.HTTP_201_CREATED)
	

# @api_view(['GET'])
# @renderer_classes((JSONRenderer, BrowsableAPIRenderer))
# def get_meu_perfil (request, *args, **kwargs):
# 	perfil_logado = get_perfil_logado(request)
# 	serializer = PerfilSerializer(perfil_logado)
# 	return response.Response(serializers.data, status.HTTP_200_OK)

# def get_perfil_logado(request):
#     	return request.user.perfil






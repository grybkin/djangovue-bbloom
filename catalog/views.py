
# -*- coding: utf-8 -*-
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import api_view, list_route, action, detail_route

from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework.permissions import BasePermission, IsAdminUser, AllowAny

from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from . import models
from . import serializers

from . import snov, hunter, anymail

import requests
import json

class IsObjectOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user and not user.is_anonymous:
            return obj.user == user
        return False


# ViewSets define the view behavior.
class LeadViewSet( mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    # def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)
    @list_route(methods=['get'], url_path='domain/(?P<company>.*)')
    def domain(self, request, company):
        """
        Obtain domain name from company name with phantombuster
        """

        return Response({'company': company})

    @list_route(methods=['get'], url_path='get_email/(?P<providers>.*)/(?P<firstName>.*)/(?P<lastName>.*)/(?P<domain>.*)')
    def get_email(self, request, providers, firstName, lastName, domain):
        """
        Validate users with providers. Allowed provider values are
        'snov', 'anymail', and 'hunter'
        """
        # provider = request.query_params.get("provider", provider)
        # domain = request.query_params.get("domain", None)
        # firstName = request.query_params.get("firstName", None)
        # lastName = request.query_params.get("lastName", None)
        res = {}
        for provider in providers.split(','):
            if provider == 'snov':
                res['snov'] = snov.get_email_finder(domain, firstName, lastName)
            elif provider == 'hunter':
                res['hunter'] = hunter.get_email_finder(domain, firstName, lastName)
            elif provider == 'anymail':
                res['anymail'] = anymail.get_email_finder(domain, firstName, lastName)
            else:
                res['provider'] = {'error': 'provider not supported: {}'.format(provider)}

        return Response(res)

    @list_route(methods=['get'], url_path='validate_email/(?P<email>.*)/(?P<ip_address>.*)')
    def validate_email(self, request, email, ip_address):
        """
        Validate user email with zerobounce.
        """
        params = {
            'email': email,
            'ip_address': ip_address,
            'api_key': '2b3c798fde3a4bdaae56a2a372d379c1'
        }

        res = requests.get('https://api.zerobounce.net/v2/validate', params=params)

        return Response(json.loads(res.text))
 
    @list_route(methods=['post'], url_path='get_domain')
    def get_domain(self, request):
        """
        Get domain name from phantombuster.
        Required parameters are 'companies'. Optional is 'blacklist'
        """
        


        return Response({'error': 'This endpoint is being deprecated'})

    queryset = models.Lead.objects.all()
    serializer_class = serializers.LeadSerializer
    permission_classes = (AllowAny|IsAdminUser,)



@csrf_exempt
@api_view(['GET', 'POST'])
def lead_list(request):
    """
    List  leads, or create a new lead.
    """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        leads = Lead.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(leads, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = LeadSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()
        
        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/leads/?page=' + str(nextPage), 'prevlink': '/leads/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def lead_detail(request, pk):
    """
    Retrieve, update or delete a lead instance.
    """
    try:
        lead = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LeadSerializer(lead,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LeadSerializer(lead, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        lead.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


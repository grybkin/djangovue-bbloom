
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

from . import snov

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

    @list_route(methods=['get'], url_path='validate/(?P<provider>.*)/(?P<firstName>.*)/(?P<lastName>.*)/(?P<domain>.*)')
    def validate(self, request, provider, firstName, lastName, domain):
        """
        Validate users with providers. Allowed provider values are
        'snov', 'anymail', 'zerobounce', and 'hunter'
        """
        # provider = request.query_params.get("provider", provider)
        # domain = request.query_params.get("domain", None)
        # firstName = request.query_params.get("firstName", None)
        # lastName = request.query_params.get("lastName", None)

        if provider == 'snov':
            print('Validating with snov')

            return Response(snov.get_email_finder(domain, firstName, lastName))

        elif provider == 'hunter':
            pass
        elif provider == 'anymail':
            pass
        elif provider == 'zerobounce':
            pass
        else:
            return Response({'error': 'provider not supported: {}'.format(provider)})

        return Response({'error': 'Cannot process the request for provider {} and username {}'.format(provider, username)})

        
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


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, ValidationError, NotFound
from .models import Url, url_max_len
from .serializers import UrlSerializer
from validators import url
from uuid import uuid4
from django.db import IntegrityError, transaction

from random import choice

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/',
        'Shorten URL': '/create',
        'Get long URL': '/find'
    }

    return Response(api_urls)

from rest_framework import serializers
from rest_framework import status

@api_view(['POST'])
def new_url(request):
    def create_url_from_short(short: str):
        return request.build_absolute_uri(location="/") + "shrt/" + short
    
    new_url = request.data
    if not isinstance(new_url, str):
        raise ValidationError("Invalid value type, url to shorten (in request body) should be a string")

    if not url(new_url):
        raise ValidationError("Invalid url provided")
    
    if len(new_url) > url_max_len:
        raise ValidationError("Long URL is too long to serialize")

    url_object = {"full_url" : new_url}

    if Url.objects.filter(**url_object).exists():
        old_url = Url.objects.get(**url_object)
        return Response(old_url.short_url)
    
    while(True):
        short_url = str(uuid4()).replace('-','')[:8]
        short_url_object = {"short_url": create_url_from_short(short_url)}
        try:
            with transaction.atomic():
                if Url.objects.filter(**short_url_object).exists():
                    continue
                else:
                    url_object.update(short_url_object)
                    url_pair = UrlSerializer(data=url_object)

                    if not url_pair.is_valid():
                        raise serializers.ValidationError("This data could not have been serialized")
                    url_pair.save()

                    return Response(short_url_object["short_url"])
        except IntegrityError:
            continue
    

@api_view(['GET'])
def find_url(request):
    short_url = request.query_params.get("shrt")
    if not short_url:
        raise ParseError("No query parameter provided: shrt (should be: string)")
    
    if not url(short_url):
        raise ValidationError("Invalid url provided")

    url_object = {"short_url": short_url}
    if not Url.objects.filter(**url_object).exists():
        raise NotFound("No long url matching this short url found")

    full_url_object = Url.objects.get(**url_object)
        
    return Response(full_url_object.full_url)
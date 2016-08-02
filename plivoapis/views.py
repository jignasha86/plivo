from django.views.decorators.csrf import csrf_exempt
from plivoapis.models import PhoneNumber
from plivoapis.serializers import PhoneNumberSerializer
from plivoapis.serializers import PlivoSerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import exceptions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from plivoapis.authentication import PlivoAuthentication
from django.core.cache import cache

@api_view(['POST'])
@authentication_classes((PlivoAuthentication,))
def inbound_sms(request):
    """
    Inbound sms
    """
    try:
        output = {'message':'','error':''}
        code = 400
        if 'is_anonymous' in dir(request.user) and request.user.is_anonymous():
           raise exceptions.AuthenticationFailed('Unauthenticated')
        serializer = PlivoSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           try:
               number = PhoneNumber.objects.filter(number=serializer.data['to'], account_id=request.user.id)[0]
           except PhoneNumber.DoesNotExist:
                  output['error'] = 'to parameter not found'
                  return Response(output, status=code)
           except IndexError:
                  output['error'] = 'to parameter not found'
                  return Response(output, status=code)

           if serializer.data['text'].rstrip('\r\n') == 'STOP':
              key = serializer.data['frm']+'-'+serializer.data['to']
              if cache.get(key) is None:
                 cache.set(key, serializer.data['text'], timeout=14400) 

           output['message'] = 'inbound sms ok'
           return Response(output)

        else:
             for error in serializer.errors:
                 if 'required' in serializer.errors[error][0]:
                    msg = error + ' is missing'
                 else:
                      msg = error + ' is invalid'
             output['error'] = msg
             return Response(output, status=code)                   
    except Exception as ex:
           output['error'] = "unknown failure"
           if ex.status_code == 401:
              output['error'] = ex.detail
              code = 403
           return Response(output, status=code)  


@api_view(['POST'])
@authentication_classes((PlivoAuthentication,))
def outbound_sms(request):
    """
    Outbound sms
    """
    try:
        output = {'message':'','error':''}
        code = 400
        if  'is_anonymous' in dir(request.user) and request.user.is_anonymous():
           raise exceptions.AuthenticationFailed('Unauthenticated')

        serializer = PlivoSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           try:
               number = PhoneNumber.objects.filter(number=serializer.data['frm'], 
                                                   account_id=request.user.id)[0]
           except PhoneNumber.DoesNotExist:
                  output['error'] = 'frm parameter not found'
                  return Response(output, status=code)
           except IndexError:
                  output['error'] = 'frm parameter not found'
                  return Response(output, status=code)

           key = serializer.data['to']+'-'+serializer.data['frm']
           if cache.get(key) is not None:
              output['error'] = 'sms from %s to %s blocked by STOP request' % (
                                 serializer.data['frm'], serializer.data['to'])
              return Response(output, status=code)

           frm_key = 'outbound-'+serializer.data['frm']
           if cache.get(frm_key) is None:
              cache.set(frm_key, 1, 86400)
           elif int(cache.get(frm_key)) > 50:
                output['error'] = 'limit reached for from %s' % (
                                   serializer.data['frm'],)
                return Response(output, status=code)
           else:
                cache.incr(frm_key)
   
           output['message'] = 'outbound sms ok'
           return Response(output)

        else:
             for error in serializer.errors:
                 if 'required' in serializer.errors[error][0]:
                    msg = error + ' is missing'
                 else:
                      msg = error + ' is invalid'
             output['error'] = msg
             return Response(output, status=code)
    except Exception as ex:
           output['error'] = "unknown failure"
           if ex.status_code == 401:
              output['error'] = ex.detail
              code = 403
           return Response(output, status=code)


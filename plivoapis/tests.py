from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import base64

class InboundTests(APITestCase):
    def test_valid_data(self):
        """
        Ensure data is in valid check works
        """

        url = reverse('inbound')
        data = {'frm':'1234','to':'123'}
        credentials = base64.b64encode('plivo1:20S0KPNOIM')
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message":"","error":"text is missing"})

        url = reverse('inbound')
        data = {'frm':'1234','to':'123','text':'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message":"","error":"frm is invalid"})

    def test_authentication(self):
        url = reverse('inbound')
        data = {'to':'4924195509198','frm':'441224459426', 'text':'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)
       
        url = reverse('inbound')
        data = {'to':'4924195509198','frm':'441224459426', 'text':'test'}
        credentials = base64.b64encode('plivo1:test')
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_redis_entry(self):
        """
        Test for redis entries 
        """
      
        url = reverse('inbound')
        data = {'to':'4924195509198','frm':'441224459426', 'text':'STOP'}
        credentials = base64.b64encode('plivo1:20S0KPNOIM')
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        url = reverse('inbound')
        data = {'to':'441224459426','frm':'4924195509198', 'text':'hello'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message":"","error":"sms from %s to %s blocked by STOP request" % (data['frm'], data['to'])})
        

class OutboundTests(APITestCase):
    def test_valid_data(self):
        """
        Ensure data is in valid check works
        """

        url = reverse('outbound')
        data = {'frm':'1234','to':'123'}
        credentials = base64.b64encode('plivo1:20S0KPNOIM')
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message":"","error":"text is missing"})

        url = reverse('inbound')
        data = {'frm':'1234','to':'123','text':'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message":"","error":"frm is invalid"})

    def test_authentication(self):
        url = reverse('outbound')
        data = {'to':'4924195509198','frm':'441224459426', 'text':'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)        

        url = reverse('outbound')
        data = {'to':'4924195509198','frm':'441224459426', 'text':'test'}
        credentials = base64.b64encode('plivo1:test')
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)


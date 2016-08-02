from rest_framework import serializers
from plivoapis.models import Account, PhoneNumber

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'auth_id', 'username')

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('id', 'number', 'account')

class PlivoSerializer(serializers.Serializer):
      frm = serializers.CharField(required=True,
                                  min_length=6,
                                  max_length=16)

      to = serializers.CharField(required=True,
                                  min_length=6,
                                  max_length=16)

      text = serializers.CharField(required=True,
                                  min_length=1,
                                  max_length=120)

      def update(self, instance, validated_data):
        """
        Create or update a new plivi instance, given a dictionary
        of deserialized field values.
        """
        if instance:
           instance.frm = validated_data.get('frm', instance.frm)
           instance.to = validated_data.get('to', instance.to)
           instance.text = validated_data.get('text', instance.text)
           instance.save()
           return instance

      def create(self, validated_data):
          return validated_data

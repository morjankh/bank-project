from rest_framework import serializers
from core.models import Customer  # Import the Customer model from core

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is write-only

    class Meta:
        model = Customer  # Specify the model
        fields = ['id', 'username', 'email', 'phone_number', 'address', 'password']  # Fields to include

    def create(self, validated_data):
        # Create a new Customer with encrypted password
        customer = Customer.objects.create(**validated_data)
        customer.set_password(validated_data['password'])
        customer.save()
        return customer

    def update(self, instance, validated_data):
        # Update an existing Customer with encrypted password
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance

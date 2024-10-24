from django.core.mail import send_mail
from rest_framework import serializers
from core.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'phone_number', 'address', 'password']

    def create(self, validated_data):
        customer = Customer.objects.create(**validated_data)
        customer.set_password(validated_data['password'])
        customer.save()
        # self.send_welcome_email(customer)
        return customer

    # def send_welcome_email(self, customer):
    #     subject = 'Welcome to Our Platform!'
    #     message = f'Hi {customer.username},\n\nWelcome to our platform! We are excited to have you.'
    #     from_email = 'your-email@gmail.com'  # Replace with your default sender email
    #     recipient_list = [customer.email]
    #
    #     # Send the email
    #     send_mail(subject, message, from_email, recipient_list)

    def update(self, instance, validated_data):
        """ Update an existing Customer with encrypted password"""
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance

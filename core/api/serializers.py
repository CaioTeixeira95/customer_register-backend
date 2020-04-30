from ..models import Customer, Addresses
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.models import User


class AddressesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Addresses
        fields = [
            'id',
            'street',
            'zip_code',
            'neighborhood',
            'city',
            'state',
            'country',
        ]


class CustomerSerializer(serializers.ModelSerializer):
    addresses = AddressesSerializer(many=True, source='addresses_set')

    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'document',
            'rg',
            'birthday',
            'phone',
            'addresses',
            'user',
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        with transaction.atomic():
            customer = Customer.objects.create(
                name=validated_data['name'],
                document=validated_data['document'],
                rg=validated_data['rg'],
                birthday=validated_data['birthday'],
                phone=validated_data['phone'],
                user=validated_data['user'],
            )

            Addresses.objects.bulk_create([
                Addresses(**address, customer=customer)
                for address in validated_data['addresses_set']
            ])

        return customer

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.name = validated_data['name']
            instance.document = validated_data['document']
            instance.rg = validated_data['rg']
            instance.birthday = validated_data['birthday']
            instance.phone = validated_data['phone']

            instance.save()

            exclude_addresses = instance.addresses_set.filter(
                customer=instance
            ).exclude(
                id__in=[
                    address.get('id')
                    for address in validated_data['addresses_set']
                    if address.get('id', None) is not None
                ]
            )

            exclude_addresses.delete()

            updated_addresses = instance.addresses_set.all()

            for address in updated_addresses:
                for ad in validated_data['addresses_set']:
                    if address.id == ad.get('id', None):
                        address.street = ad['street']
                        address.zip_code = ad['zip_code']
                        address.neighborhood = ad['neighborhood']
                        address.city = ad['city']
                        address.state = ad['state']
                        address.country = ad['country']
                        address.save()
                        break

            Addresses.objects.bulk_create([
                Addresses(**address, customer=instance)
                for address in validated_data['addresses_set']
                if address.get('id', None) is None
            ])

        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
        ]

    def create(self, validated_data):
        with transaction.atomic():
            user = super().create(validated_data)
            user.set_password(validated_data['password'])
            user.save()
        return user

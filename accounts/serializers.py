from rest_framework_gis import serializers

from .models import Account


class accountSerializer(serializers.GeoFeatureModelSerializer):

    class Meta:
        """Marker serializer meta class."""

        fields = '__all__'
        geo_field = "position"
        model = Account

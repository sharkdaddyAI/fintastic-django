from django.utils.timezone import now
from rest_framework import serializers
from favorite.models import Favorite

class ToUpperCaseCharField(serializers.CharField):
    def to_representation(self, value):
        return value.upper()

class FavoriteSerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()
    ticker = ToUpperCaseCharField()
    
    class Meta:
        model = Favorite
        fields = '__all__'
        # fields = ('id', 'song', 'singer', 'last_modify_date', 'created')

    def get_days_since_created(self, obj):
        return (now() - obj.created).days
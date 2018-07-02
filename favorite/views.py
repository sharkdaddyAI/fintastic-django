# Create your views here.
from favorite.models import Favorite
from favorite.serializers import FavoriteSerializer

from rest_framework import viewsets


# Create your views here.
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
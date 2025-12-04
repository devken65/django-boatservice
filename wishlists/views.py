from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from boats.models import Boat

from .models import Wishlist
from .serializers import WishlistSerializer


class Wishlists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_wishlist = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            user_wishlist,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        # 05:30


class WishlistToggle(APIView):
    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_boat(self, pk):
        try:
            return Boat.objects.get(pk=pk)
        except Boat.DoesNotExist:
            raise NotFound

    def put(self, request, pk, boat_pk):
        wishlist = self.get_list(pk, request.user)
        boat = self.get_boat(boat_pk)
        if wishlist.boat.filter(pk=boat.pk).exists():
            wishlist.boat.remove(boat)
        else:
            wishlist.boat.add(boat)
        return Response(status=HTTP_200_OK)

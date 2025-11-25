from django.conf import settings
from django.db import transaction
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from categories.models import Category
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer

from .models import Amenity, Boat
from .serializer import AmenitySerializer, BoatDetailSerializer, BoatListSerializer


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound  # noqa: B904

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity.data))
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Boats(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_boats = Boat.objects.all()
        serializer = BoatListSerializer(
            all_boats,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = BoatDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.SEAPLATFORMS:
                    raise ParseError("Boat category should be boat. not seaplatform")
            except Category.DoesNotExist:
                raise ParseError("Category does not exist")
            try:
                with transaction.atomic():
                    boat = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    amenities = request.data.get("amenities")
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        boat.amenities.add(amenity)
                    serializer = BoatDetailSerializer(boat)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not Found")
        else:
            return Response(serializer.errors)


class BoatDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Boat.objects.get(pk=pk)
        except Boat.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        boat_object = self.get_object(pk)
        serializer = BoatDetailSerializer(
            boat_object,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        boat = self.get_object(pk)
        if boat.owner != request.user:
            raise PermissionDenied
        # Challenge!

    def delete(self, request, pk):
        boat = self.get_object(pk)
        if boat.owner != request.user:
            raise PermissionDenied
        boat.Delete()
        return Response(status=HTTP_204_NO_CONTENT)


class BoatReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Boat.objects.get(pk=pk)
        except Boat.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        boat = self.get_object(pk)
        serializer = ReviewSerializer(
            boat.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                boat=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)


class BoatPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Boat.objects.get(pk=pk)
        except Boat.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        boat = self.get_object(pk)
        if request.user != boat.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)

        if serializer.is_valid():
            photo = serializer.save(boat=boat)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

from django.db import transaction
from django.utils import timezone
from rest_framework import permissions
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from categories.models import Category
from reservations.models import Reservation
from reservations.serializers import CreateReservationSerializer, PublicReservationSerializer

from .models import Perk, Seaplatform
from .serializers import PerkSerializer, SeaplatformDetailSerializer, SeaplatformListSerializer


class Perks(APIView):
    def get(self, request):
        all_Perks = Perk.objects.all()
        serializer = PerkSerializer(all_Perks, many=True)
        return Response(serializer.data)  # noqa: F706

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, request, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)

        if serializer.is_valid():
            updated_perk = serializer.save()
            return PerkSerializer(updated_perk).data
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class SeaplatformList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # GET POST
    def get(self, request):
        all_seaplatforms = Seaplatform.objects.all()
        serializer = SeaplatformListSerializer(
            all_seaplatforms,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = SeaplatformListSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                return ParseError
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.BOATS:
                    raise ParseError("this page is for seaplatform, not boat")
            except Category.DoesNotExist:
                raise ParseError("Category does not exist")

            with transaction.atomic():
                new_seaplatform = serializer.save(
                    owner=request.user,
                    category=category,
                )

            return Response(SeaplatformDetailSerializer(new_seaplatform).data)
        else:
            return Response(serializer.errors)


class SeaplatformDetail(APIView):
    def get_object(self, pk):
        try:
            return Seaplatform.objects.get(pk=pk)
        except Seaplatform.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        seaplatform = self.get_object(pk)
        serializer = SeaplatformDetailSerializer(
            seaplatform,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        seaplatform = self.get_object(pk)
        if seaplatform.owner != request.user:
            raise PermissionDenied

        serializer = SeaplatformDetailSerializer(
            seaplatform,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if serializer.is_valid():
            update_seaplatform = serializer.save(owner=request.user)

            return Response(
                SeaplatformDetailSerializer(update_seaplatform, context={"request": request}).data
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        seaplatform = self.get_object(pk)
        if seaplatform.owner != request.user:
            raise PermissionDenied
        seaplatform.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class SeaplatformReservations(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, seaplatform_pk):
        try:
            return Seaplatform.objects.get(pk=seaplatform_pk)
        except Seaplatform.DoesNotExist:
            raise NotFound

    def get(self, request, seaplatform_pk):
        # 가져오고
        seaplatform = self.get_object(seaplatform_pk)
        now = timezone.localtime(timezone.now())
        reservation = Reservation.objects.filter(
            seaplatform=seaplatform,
            kind=Reservation.ReservationKindChoices.SEAPLATFORM,
            check_in__gt=now,
        )
        serializer = PublicReservationSerializer(reservation, many=True)
        return Response(serializer.data)

    def post(self, request, seaplatform_pk):
        seaplatform = self.get_object(seaplatform_pk)
        serializer = CreateReservationSerializer(data=request.data)
        if serializer.is_valid():
            new_reservation = serializer.save(
                seaplatform=seaplatform,
                user=request.user,
                kind=Reservation.ReservationKindChoices.SEAPLATFORM,
            )
            serializer = PublicReservationSerializer(new_reservation)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)


class SeaplatformReservationDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, seaplatform_pk, reservation_pk):
        reservation = Reservation.objects.get(pk=reservation_pk, seaplatform_id=seaplatform_pk)
        serializer = PublicReservationSerializer(reservation)
        return Response(serializer.data)

    def put(self, request, seaplatform_pk, reservation_pk):
        reservation = Reservation.objects.get(pk=reservation_pk, seaplatform_id=seaplatform_pk)
        serializer = PublicReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, seaplatform_pk, reservation_pk):
        reservation = Reservation.objects.get(pk=reservation_pk, seaplatform_id=seaplatform_pk)
        if reservation.user != request.user:
            raise PermissionDenied
        reservation.delete()
        return Response(status=HTTP_200_OK)

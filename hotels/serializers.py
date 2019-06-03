from datetime import datetime

from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Hotel, Booking


class HotelsListSerializer(serializers.ModelSerializer):
	details = serializers.HyperlinkedIdentityField(
		view_name = "hotel-details",
		lookup_field = "id",
		lookup_url_kwarg = "hotel_id"
		)
	class Meta:
		model = Hotel
		fields = ['name', 'details']


class HotelDetailsSerializer(serializers.ModelSerializer):
	book = serializers.HyperlinkedIdentityField(
		view_name = "book-hotel",
		lookup_field = "id",
		lookup_url_kwarg = "hotel_id"
		)
	class Meta:
		model = Hotel
		fields = ["name", "location", "price_per_night", "book"]


class BookHotelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['check_in', 'number_of_nights']


class BookingDetailsSerializer(serializers.ModelSerializer):
	hotel = HotelsListSerializer()
	cancel = serializers.HyperlinkedIdentityField(
		view_name = "cancel-booking",
		lookup_field = "id",
		lookup_url_kwarg = "booking_id"
		)
	modify = serializers.HyperlinkedIdentityField(
		view_name = "modify-booking",
		lookup_field = "id",
		lookup_url_kwarg = "booking_id"
		)
	class Meta:
		model = Booking
		fields = ["hotel", "check_in", 'number_of_nights', 'cancel', 'modify']


class PastBookingDetailsSerializer(serializers.ModelSerializer):
	hotel = serializers.StringRelatedField()
	class Meta:
		model = Booking
		fields = ["hotel", "check_in", 'number_of_nights']


class UserSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()
	past_bookings = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ["username", "name", "email", "past_bookings"]

	def get_name(self, obj):
		return "%s %s"%(obj.first_name, obj.last_name)

	def get_past_bookings(self, obj):
		today = datetime.today()
		bookings = obj.bookings.filter(check_in__lt=today)
		return PastBookingDetailsSerializer(bookings, many=True).data







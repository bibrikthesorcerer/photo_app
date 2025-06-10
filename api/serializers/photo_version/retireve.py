from rest_framework import serializers

from models_app.models import PhotoVersion
from api.serializers.review_ticket import RetrieveReviewTicketSerializer


class RetrievePhotoVersionSerializer(serializers.ModelSerializer):
    review_tickets = RetrieveReviewTicketSerializer(many=True)
    class Meta:
        model = PhotoVersion
        fields = '__all__'
from rest_framework import serializers

from models_app.models import ReviewTicket


class RetrieveReviewTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewTicket
        fields = ['id', 'result', 'commentary', 'is_seen', 'created_at']
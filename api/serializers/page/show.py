from rest_framework import serializers

class PageSerializer(serializers.Serializer):
    total_pages = serializers.IntegerField(source='paginator.num_pages')
    page = serializers.IntegerField(source='number')
    per_page = serializers.IntegerField(source='paginator.per_page')
    has_next = serializers.BooleanField()
    has_previous = serializers.BooleanField()

    def __init__(self, objects_serializer: serializers.Serializer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['objects'] = objects_serializer(many=True, source='object_list', context=self.context)
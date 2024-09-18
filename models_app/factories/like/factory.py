import factory

class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'models_app.Like'
    
    # user
    # photo
    deleted_at = None
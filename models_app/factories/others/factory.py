import factory
from models_app.factories.user_profile import UserProfileFactory
from models_app.factories.photo import PhotoFactory
from models_app.factories.comment import CommentFactory, ThreadsCommentFactory
from models_app.factories.like import LikeFactory


class ComplexUserFactory(UserProfileFactory):
    class Meta:
        skip_postgeneration_save = True

    @factory.post_generation
    def photos(self, create, extracted, **kwargs):
        if not create:
            return

        num_photos = kwargs.pop("num_photos", 0)
        photo_status = kwargs.pop("photo_status", None)
        comments_per_photo = kwargs.pop("comments_per_photo", 0)
        comment_thread_depth = kwargs.pop("comment_thread_depth", 0)
        likes_per_photo = kwargs.pop("likes_per_photo", 0)

        photo_kwargs = {"user": self}
        if photo_status:
            photo_kwargs[photo_status] = True

        for _ in range(num_photos):
            photo = PhotoFactory(**photo_kwargs, **kwargs)

            for _ in range(comments_per_photo):
                if comment_thread_depth > 0:
                    ThreadsCommentFactory(
                        photo=photo,
                        user=factory.LazyAttribute(lambda c: c.photo.user),
                        create_thread__thread_depth=comment_thread_depth,
                    )
                else:
                    CommentFactory(
                        photo=photo, user=factory.LazyAttribute(lambda c: c.photo.user)
                    )

            for _ in range(likes_per_photo):
                LikeFactory(photo=photo)

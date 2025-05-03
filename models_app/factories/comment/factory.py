import factory
from django.utils.timezone import now
from factory import fuzzy
from factory.declarations import LazyAttribute, SubFactory

from models_app.factories.user_profile import UserProfileFactory
from models_app.factories.photo import PhotoFactory


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "models_app.Comment"

    user = SubFactory(UserProfileFactory)
    photo = SubFactory(PhotoFactory)
    text = fuzzy.FuzzyText(length=256)
    parent = None
    pub_date = fuzzy.FuzzyDateTime(start_dt=now().replace(year=2024))
    deleted_at = None

    class Params:
        deleted = factory.Trait(
            deleted_at=LazyAttribute(lambda _: now())
        )
        with_parent = factory.Trait(
            parent=SubFactory("models_app.factories.CommentFactory")
        )

    @factory.post_generation
    def children(self, create, extracted, **kwargs):
        if not create:
            return

        # append given children or create new ones
        if extracted:
            for child in extracted:
                child.parent = self
                child.save()
        elif kwargs.get("num_children") is not None:
            for _ in range(kwargs["num_children"]):
                CommentFactory(parent=self, photo=self.photo)


class ChildCommentFactory(CommentFactory):
    parent = SubFactory("models_app.factories.CommentFactory")


class ThreadsCommentFactory(CommentFactory):
    @factory.post_generation
    def create_thread(self, create, extracted, **kwargs):
        if create and kwargs.get("thread_depth") is not None:
            parent_comment = self
            for i in range(kwargs.get("thread_depth")):
                parent_comment = CommentFactory(parent=parent_comment, photo=parent_comment.photo)

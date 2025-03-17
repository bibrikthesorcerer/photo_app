from enum import StrEnum
from viewflow.fsm import State
from django.utils import timezone

from models_app.models import Photo
from main_app.services import CreateReviewTicket


class ModerationStage(StrEnum):
    ON_MODERATION = Photo.ON_MODERATION
    DENIED = Photo.DENIED
    APPROVED = Photo.APPROVED
    TO_BE_DELETED = Photo.TO_BE_DELETED

    def __lt__(self, other):
        self.value < other.value


class PhotoModerationFlow:
    stage = State(ModerationStage, default=ModerationStage.ON_MODERATION)

    def __init__(self, photo):
        self.photo = photo

    def _create_review_ticket(self, moderator, commentary="", **kwargs):
        self.review_ticket = CreateReviewTicket.execute({
            "object_id": self.photo.id,
            "moderator": moderator,
            "commentary": commentary,
            "result": self.photo.status
        })

    @stage.getter()
    def _get_photo_status(self):
        return ModerationStage(self.photo.status)

    @stage.transition(source=ModerationStage.ON_MODERATION, target=ModerationStage.DENIED)
    def deny(self, **kwargs):
        self.photo.pub_date = None
        self.photo.status = Photo.DENIED
        self.photo.save()
        self._create_review_ticket(**kwargs)

    @stage.transition(source=ModerationStage.ON_MODERATION, target=ModerationStage.APPROVED)
    def approve(self, **kwargs):
        self.photo.pub_date = timezone.now()
        self.photo.status = Photo.APPROVED
        self.photo.save()
        self._create_review_ticket(**kwargs)

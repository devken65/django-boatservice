from django.db import models

from common.models import CommonModel


class ChattingRoom(CommonModel):
    user = models.ManyToManyField(
        "accounts.User",
    )

    def __str__(self):
        return "Chatting Room"


class Message(CommonModel):
    text = models.TextField()
    user = models.ForeignKey(
        "accounts.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    boat = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user} says: {self.text}"

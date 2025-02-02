"""
Interactions with the aa-discordbot application

https://github.com/Solar-Helix-Independent-Transport/allianceauth-discordbot
"""

from aadiscordbot.tasks import send_message
from discord import Embed

from dens.models import MercenaryDenReinforcedNotification


def send_reinforced_notification_to_user(
    notification: MercenaryDenReinforcedNotification,
):
    """Sends a discord message a user warning that a mercenary den has been reinforced"""

    user = notification.den.owner.character_ownership.user

    e = Embed(
        title="Mercenary Den reinforced",
    )
    e.add_field(name="Location", value=notification.den.location.name)
    e.add_field(name="Reinforced by", value=notification.reinforced_by.character_name)
    e.add_field(
        name="Exit reinforcement", value=notification.exit_reinforcement.isoformat()
    )

    send_message(user=user, embed=e)

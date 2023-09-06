from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import PreBaseCharityDonation


class Donation(PreBaseCharityDonation):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'Пожертвование от пользователя id {self.user_id}'

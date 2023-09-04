from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import PreBaseCharityDonation


class Donation(PreBaseCharityDonation):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id')) 
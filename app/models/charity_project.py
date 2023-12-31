from sqlalchemy import Column, String, Text

from app.core.db import PreBaseCharityDonation


class CharityProject(PreBaseCharityDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return f'Благотворительный проект "{self.name}"'

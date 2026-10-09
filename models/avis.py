from sqlalchemy import Column, Integer, String
from Config.db import Base


class Avis(Base):
    __tablename__ = "avis"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, foreign_key="users.id")
    avis = Column(String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "avis": self.avis
        }
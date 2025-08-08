from sqlalchemy import Column, Index, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, declarative_base, mapped_column
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class NewsRadarXPost(Base):
    __tablename__ = "news_radar_X_post"
    __table_args__ = (Index("link", "link", unique=True),)

    id = mapped_column(BIGINT(20), primary_key=True)
    username = mapped_column(String(255), nullable=False)
    text_ = mapped_column("text", Text, nullable=False)
    link = mapped_column(String(255), nullable=False)
    date = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp() ON UPDATE current_timestamp()"),
    )

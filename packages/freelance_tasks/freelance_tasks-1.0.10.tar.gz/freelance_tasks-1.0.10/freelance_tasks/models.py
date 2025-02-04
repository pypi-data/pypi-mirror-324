from datetime import datetime

from pydantic import BaseModel, Field


class ProjectOwner(BaseModel):
    url: str
    username: str
    img: str
    online_at: datetime
    full_name: str
    tags: list[str]


class Project(BaseModel):
    id: int
    url: str
    title: str
    description: str
    public_at: datetime
    tags: list[str]
    price: float | None
    owner: ProjectOwner


class Projects(BaseModel):
    count: int = Field(default=0)
    items: list[Project] = Field(default_factory=list)


class User(BaseModel):
    html: str
    username: str
    avatar: str
    name: str
    profession: str
    description: str
    tags: list[str]

    def to_message(self):
        tags_text = ", ".join(self.tags) if self.tags else "Нет тегов"
        message = (
            f"👤 <b>{self.name}</b> (@{self.username})\n"
            f"💼 <i>{self.profession}</i>\n\n"
            f"📝 <b>О себе:</b>\n{self.description}\n\n"
            f"🏷 <b>Теги:</b> {tags_text}"
        )

        return message

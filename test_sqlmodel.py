from sqlmodel import Field, SQLModel


class RegInfo(SQLModel):
    id: str = Field(primary_key=True)
    reg_date: str

class Purchases(SQLModel):
    user_id: str = Field(foreign_key="reginfo.id")



r = RegInfo(id="id", reg_date="kuku")
print(r.mode)

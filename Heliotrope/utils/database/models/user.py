from tortoise import Model, fields


class User(Model):
    user_id = fields.BigIntField(pk=True, description="discord user id")

    class Meta:
        table = "users"
        table_desc = "Table of user datas"

    def __int__(self):
        return self.user_id

    def __repr__(self):
        return f"<User id={self.user_id} >"

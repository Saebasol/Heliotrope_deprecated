from tortoise import Model, fields


class User(Model):
    user_id = fields.BigIntField(pk=True, description="discord user id")
    download_count = fields.IntField(default=0)

    class Meta:
        table = "users"
        table_desc = "Table of user datas"

    def __int__(self):
        return self.user_id

    def __repr__(self):
        return (
            "<User"
            + f" id={self.user_id}"
            + f" download_count={self.download_count}"
            + ">"
        )
from tortoise import Model, fields


class RequestCount(Model):
    index: int = fields.IntField(pk=True)
    count: int = fields.IntField()

    class Meta:
        table = "ranking"
        table_desc = "Table of hitomi number of index requests"
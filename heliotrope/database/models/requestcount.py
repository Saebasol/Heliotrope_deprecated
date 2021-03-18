from tortoise import Model, fields


class RequestCount(Model):
    index: int = fields.IntField(pk=True)
    title: str = fields.CharField(255)
    count: int = fields.IntField()

    class Meta:
        table = "ranking"
        table_desc = "Table of hitomi number of index requests"

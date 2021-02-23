from tortoise import Model, fields


class Ranking(Model):
    index = fields.CharField(pk=True, max_length=10)
    count = fields.IntField()

    class Meta:
        table = "ranking"
        table_desc = "Table of hitomi ranking"

    def __str__(self):
        return self.index

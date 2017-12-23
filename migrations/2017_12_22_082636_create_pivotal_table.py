from orator.migrations import Migration


class CreatePivotalTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('pivotals') as table:
            table.increments('id')
            table.string('pivotal_id', 64)
            table.string('title', 255)
            table.string('type', 20)
            table.text('description')
            table.string('status', 20)
            table.text('json_data')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('pivotals')

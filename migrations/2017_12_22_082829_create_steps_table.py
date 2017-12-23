from orator.migrations import Migration


class CreateStepsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('steps') as table:
            table.increments('id')
            table.string('test_library_id', 64)
            table.text('steps')
            table.string('status', 20)
            table.text('message')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('steps')

from orator.migrations import Migration


class CreateInstancesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('instances') as table:
            table.increments('id')
            table.string('pratitest_set_id', 64)
            table.string('pratitest_lib_id', 64)
            table.string('status', 20)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('instances')

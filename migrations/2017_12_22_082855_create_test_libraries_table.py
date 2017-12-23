from orator.migrations import Migration


class CreateTestLibrariesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('test_libraries') as table:
            table.increments('id')
            table.string('pratitest_lib_id', 64)
            table.string('pratitest_id', 64)
            table.string('title', 255)
            table.text('gherkin')
            table.string('status', 20)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('test_libraries')

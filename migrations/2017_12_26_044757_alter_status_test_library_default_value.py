from orator.migrations import Migration


class AlterStatusTestLibraryDefaultValue(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('test_libraries') as table:
            table.string('status', 20).default('No Run').change()
            pass

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('test_libraries') as table:
            table.string('status', 20).default('No Run').change()
            pass

from orator.migrations import Migration


class AlterTestStatusPractitestDefaultValue(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('practitest') as table:
            table.string('test_status', 20).default('No Run').change()
            pass

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('practitest') as table:
            table.string('test_status', 20).default('No Run').change()
            pass

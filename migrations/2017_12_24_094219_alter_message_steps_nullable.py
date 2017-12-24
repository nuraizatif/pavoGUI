from orator.migrations import Migration


class AlterMessageStepsNullable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('steps') as table:
            table.text('message').nullable().change()
            pass

    def down(self):
        """
        Revert the migrations.
        """
        cols = [ 'message' ]
        with self.schema.table('steps') as table:
            for col in enumerate(cols):
                if col in table.get_columns():
                    table.string('message').change()
            pass

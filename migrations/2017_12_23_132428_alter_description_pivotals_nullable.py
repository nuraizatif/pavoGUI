from orator.migrations import Migration


class AlterDescriptionPivotalsNullable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('pivotals') as table:
            table.text('description').nullable().change()

    def down(self):
        """
        Revert the migrations.
        """
        cols = [ 'description' ]
        with self.schema.table('pivotals') as table:
            for col in enumerate(cols):
                if col in table.get_columns():
                    table.text('description').change()

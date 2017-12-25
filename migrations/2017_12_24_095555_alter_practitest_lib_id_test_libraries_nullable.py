from orator.migrations import Migration


class AlterPractitestLibIdTestLibrariesNullable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('test_libraries') as table:
            table.string('pratitest_lib_id').nullable().change()
            pass

    def down(self):
        """
        Revert the migrations.
        """
        cols = [ 'pratitest_lib_id' ]
        with self.schema.table('test_libraries') as table:
            for col in enumerate(cols):
                if col in table.get_columns():
                    table.string('pratitest_lib_id').change()
            pass

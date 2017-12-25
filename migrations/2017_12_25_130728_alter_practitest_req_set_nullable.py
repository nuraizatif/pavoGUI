from orator.migrations import Migration


class AlterPractitestReqSetNullable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('practitest') as table:
            table.string('pratitest_req_id').nullable().change()
            table.string('pratitest_set_id').nullable().change()
            pass

    def down(self):
        """
        Revert the migrations.
        """
        cols = [ 'pratitest_req_id', 'pratitest_set_id' ]
        with self.schema.table('practitest') as table:
            for col in enumerate(cols):
                if col in table.get_columns():
                    table.string('pratitest_lib_id').change()
                    table.string('pratitest_set_id').change()
            pass

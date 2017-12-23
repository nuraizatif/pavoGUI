from orator.migrations import Migration


class CreatePractitestTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('practitest') as table:
            table.increments('id')
            table.string('pratitest_req_id', 64)
            table.string('pratitest_set_id', 64)
            table.string('pivotals_id', 64)
            table.string('status', 20)
            table.string('test_phase', 20)
            table.string('test_level', 20)
            table.string('product_component', 20)
            table.string('os', 20)
            table.string('test_case', 20)
            table.string('test_type', 20)
            table.string('release', 255)
            table.string('test_status', 20)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('practitest')

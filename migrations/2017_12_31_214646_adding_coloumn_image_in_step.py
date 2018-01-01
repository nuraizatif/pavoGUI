from orator.migrations import Migration


class AddingColoumnImageInStep(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('steps') as table:
            table.string('image_dir').nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('steps') as table:
            table.string('image_dir').nullable()

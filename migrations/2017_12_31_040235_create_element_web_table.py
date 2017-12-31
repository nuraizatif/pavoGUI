from orator.migrations import Migration


class CreateElementWebTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('element_web') as table:
            table.increments('id')
            table.string('name', 100)
            table.string('type', 100)
            table.string('value', 255)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('element_web')

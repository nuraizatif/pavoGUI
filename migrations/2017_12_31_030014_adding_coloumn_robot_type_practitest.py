from orator.migrations import Migration


class AddingColoumnRobotTypePractitest(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('practitest') as table:
            table.string('robot_type', 20).default('api')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('practitest') as table:
            table.string('robot_type', 20).default('api')

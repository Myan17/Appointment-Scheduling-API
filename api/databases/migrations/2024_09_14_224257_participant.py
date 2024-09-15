"""Participant Migration."""

from masoniteorm.migrations import Migration


class Participant(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("participants") as table:
            table.increments("id")
            table.string("participant_id")
            table.foreign("participant_id").references("id").on("users")
            table.string("meeting_id")
            table.foreign("meeting_id").references("id").on("meetings")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("participants")

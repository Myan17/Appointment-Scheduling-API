"""Meeting Migration."""

from masoniteorm.migrations import Migration


class Meeting(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("meetings") as table:
            table.increments("id")
            table.string("title")
            table.date("date")
            table.time("time")
            table.string("organizer")
            table.foreign("organizer").references("email").on("users")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("meetings")

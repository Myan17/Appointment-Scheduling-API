"""User Migration."""

from masoniteorm.migrations import Migration


class User(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("users") as table:
            table.increments("id")
            table.string("first_name")
            table.string("middle_name")
            table.string("surname")
            table.string("email").unique()
            table.string("cellphone")
            table.string("password")
            table.enum("gender" , ["m" , "f"])
            table.string("city")
            table.string("state")
            table.string("zipcode")
            table.string("timezone")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("users")

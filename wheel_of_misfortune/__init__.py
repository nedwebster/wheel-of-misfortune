import json
import random
from typing import List


class WheelOfMisfortune:
    """Wheel Of Misfortune, used to select QOTW candidate.

    Parameters
    ----------
    team_members: List[str]
        List of all team members

    this_week: str
        Who is assigned for this week.

    last_week: str
        Who was assigned the week before.

    available_picks: List[str]
        All possible picks for the next spin of the wheel. These values are not unique!

    """

    def __init__(self, team_members: List[str], this_week: str, last_week: str, available_picks: List[str]):
        self.team_members = team_members
        self.this_week = this_week
        self.last_week = last_week
        self.available_picks = available_picks

        if len(self.available_picks) == 0:
            self.available_picks = self.team_members

    def spin_the_wheel(self):
        """Select a member of the team to ask QOTW, and update the class attributes accordingly."""
        the_lucky_one = random.choice(self.available_picks)
        self._update_attributes(name=the_lucky_one)

        return the_lucky_one

    def _update_attributes(self, name: str):
        """Update attributes based on who was selected this week."""
        self.last_week = self.this_week
        self.this_week = name

        updated_picks = [x for x in self.available_picks if x != name]
        to_add = [x for x in self.team_members if x != name]
        updated_picks += to_add

        self.available_picks = updated_picks

    def update_config(self):
        """Update the local config file, and save the changes."""
        config = {
            "team_members": self.team_members,
            "this_week": self.this_week,
            "last_week": self.last_week,
            "available_picks": self.available_picks,
        }

        with open("wheel_of_misfortune_config.json", "w") as file:
            json.dump(config, file, indent=4)

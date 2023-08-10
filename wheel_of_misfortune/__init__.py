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

    def spin_the_wheel(self, ignore_list: List[str] = []):
        """Select a member of the team to ask QOTW, and update the class attributes accordingly."""

        available_picks = [name for name in self.available_picks if name not in ignore_list]
        the_lucky_one = random.choice(available_picks)
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

    def place_your_bets(self) -> dict:
        """Create a dictionary where the keys are members names, and the values are their probability to be selected."""

        odds_dict = {}

        for person in self.team_members:
            odds_dict[person] = self.available_picks.count(person) / len(self.available_picks)

        # sort dict and format decimals to percentages
        odds_dict = {
            k: '{:.1%}'.format(v) for k, v in
            sorted(odds_dict.items(), key=lambda item: item[1], reverse=True)
        }

        return odds_dict

    def add_new_member(self, name: str):
        if name in self.team_members:
            raise ValueError(f"{name} already in the list of players!")
        self.team_members.append(name)
        self.available_picks.append(name)
        self.update_config()

    def remove_member(self, name: str):
        self.team_members = [x for x in self.team_members if x != name]
        self.available_picks = [x for x in self.available_picks if x != name]
        self.update_config()

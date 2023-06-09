import json
import requests
import time
from datetime import date
from git import Repo

import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie, st_lottie_spinner

from wheel_of_misfortune import WheelOfMisfortune


def load_wheel() -> WheelOfMisfortune:
    with open("wheel_of_misfortune_config.json", "r") as file:
        config = json.load(file)
    wheel_of_misfortune = WheelOfMisfortune(**config)
    return wheel_of_misfortune


def load_animation(url: str):
    animation = requests.get(url)
    return animation.json()


def commit_new_config():
    try:
        repo = Repo(".")
        repo.git.add(update=True)
        commit_message = f"wheel spin on {str(date.today())}"
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
    except Exception:
        print('Some error occured while pushing the code')


if __name__ == "__main__":

    wheel_animation = load_animation("https://assets7.lottiefiles.com/packages/lf20_0qDTNXPljS.json")
    firework_animation = load_animation("https://assets3.lottiefiles.com/private_files/lf30_rjuv1b.json")

    wheel_of_misfortune = load_wheel()

    st.title("QOTW: Wheel of Misfortune")

    if st.button(label="Spin the wheel!"):
        with st_lottie_spinner(wheel_animation, speed=1.5, loop=False):
            time.sleep(4)

        selected_person = wheel_of_misfortune.spin_the_wheel()
        wheel_of_misfortune.update_config()
        st.title(f"The wheel landed on {selected_person}, congratulations!")
        st_lottie(firework_animation)
        commit_new_config()

    data = pd.DataFrame.from_dict(wheel_of_misfortune.place_your_bets(), orient="index", columns=["probability"])
    st.table(data)

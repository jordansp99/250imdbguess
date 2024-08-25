import csv
import random
import streamlit as st
import json
import re
import pandas as pd
import numpy as np
from datetime import datetime

@st.cache_data
def load_data():
    with open('clues.json', 'r') as file:
        data = json.load(file)      
        df = pd.DataFrame(columns=['Film Name', 'Clues','Film Year'])
    # Iterate over each film in the JSON data
    for film in data:
        film_name = film["Film Name"]
        clues_text = film["Clue"]

        # Extract the clues using a regular expression
        clues = re.findall(r'\d+\.\s*(.*)', clues_text)

        df = df._append({'Film Name': film_name, 'Clues': clues}, ignore_index=True)
    with open('imdb_top_250.csv') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)

    # Iterate through the rows of the CSV file
        for row in csv_reader:
            film_name = row[0]
            film_year = row[1]

            # Update the DataFrame with the film year
            # Here, we match the film name in the CSV with the JSON film names
            df.loc[df['Film Name'] == film_name, 'Film Year'] = film_year
            
    return df
def random_number_based_on_today(start, end):
    # Get today's date

    today = datetime.today()

    # Convert today's date to an integer seed
    seed = int(today.strftime('%Y%m%d'))

    # Set the random seed
    random.seed(seed)

    # Generate and return a random number within the specified range
    return random.randint(start, end)

        
df = load_data()


random_num = random_number_based_on_today(0, len(df))

if 'film_to_guess' not in st.session_state:
    st.session_state['film_to_guess'] = df['Film Name'].iloc[random_num] #get random films
if 'clues_shown' not in st.session_state:
    st.session_state['clues_shown'] = 1
if 'win' not in st.session_state:
    st.session_state['win'] = False
    

film_name = st.session_state['film_to_guess'] #film name Session state saved in variable

clues = df.loc[df['Film Name'] == film_name, 'Clues'].squeeze()
film_year = df.loc[df['Film Name'] == film_name, 'Film Year'].squeeze()

heading = st.markdown("# Guess the film")
st.write(f"Clues {st.session_state['clues_shown']}/5")


with st.form("my_form",clear_on_submit=True):
    st.markdown(f"### Year: {film_year}")

    for i in range(st.session_state['clues_shown']):
        
        st.write(f"Clue {i + 1}: {clues[i]}\n")

    st.divider()
    # Select box for user to guess the film
    option = st.selectbox(
        "Choose a film:",
        (df['Film Name'].sort_values()),
        index=None, 
    )
    print(st.session_state['film_to_guess'] )


    submit_form = st.form_submit_button("Submit")

    if submit_form:
        

        if st.session_state['film_to_guess'] == option:
            st.session_state["win"] = True
            st.session_state['clues_shown'] = 5
            print (f"Win: {st.session_state["win"]}")
            st.rerun()


        if st.session_state['clues_shown'] < len(clues) and not st.session_state["win"]:
            st.session_state['clues_shown'] += 1
            print(f"Clues shown: {st.session_state['clues_shown']}")
            print("rerun")
            st.rerun()
        
        if st.session_state['clues_shown'] == len(clues) and not st.session_state["win"]:
                st.error(f"The correct film was {st.session_state['film_to_guess']}.")

if st.session_state["win"] == True:

    st.success(f"The correct film was {film_name}.")
    st.balloons()

with st.expander("Info", icon="ℹ️"):
    st.info("The clues were generated with gemma-2-2b. Web app was developed using Streamlit.")            
        

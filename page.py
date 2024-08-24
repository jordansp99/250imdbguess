import csv
import streamlit as st
import json
import re
import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    with open('clues.json', 'r',encoding='utf-8') as file:
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
    


        
df = load_data()

if 'film_to_guess' not in st.session_state:
    st.session_state['film_to_guess'] = df['Film Name'].sample().iloc[0] #get random films

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
        print (st.session_state["win"])
  
        if st.session_state['film_to_guess'] == option:
            st.session_state["win"] = True
            st.success("Congratulations! You won!")
                        
            st.balloons()
        if st.session_state['clues_shown'] < len(clues) and not st.session_state["win"]:
            st.session_state['clues_shown'] += 1
            print(st.session_state['clues_shown'])
            print("rerun")
            st.rerun()
        
        if st.session_state['clues_shown'] == len(clues) and not st.session_state["win"]:
                st.warning(f"The correct film was {st.session_state['film_to_guess']}")

            
        
 
            
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 11:51:52 2025

@author: shahad
"""

import streamlit as st
import numpy as np
import pandas as pd
import random 
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monte Carlo Simulation", layout="centered")
st.title("🎲 Monte Carlo: Dice roll Simulation")

# Parameters
st.sidebar.header("Simulation controls")
n_dice = st.sidebar.selectbox("Number of dice", [1,2,3,4], index=0)
# Option 2: Textbox (numeric input)

#number of rolls gives option between slider and textbox 
n_rolls = st.sidebar.slider("Rolls per trial", 100, 50000, 2000, step=100)
n_rolls_input = st.sidebar.number_input("Rolls per trial (1-50000)", min_value=1, max_value=100000, value=n_rolls)
n_rolls = n_rolls_input if n_rolls_input else n_rolls

#number of trials gives option between slider and textbox
n_trials = st.sidebar.slider("Monte Carlo trials (repeat experiments)", 1, 10000, 200)
n_trials_input = st.sidebar.number_input("Number of trials (1-10000)", min_value=1, max_value=100000, value=n_trials)
n_trials = n_trials_input if n_trials_input else n_trials

run_sim = st.button("Run the simulation")



def single_experiment(n_dice, n_rolls):
    # returns array of sums for n_rolls
    rolls = np.random.randint(1, 7, size=(n_rolls, n_dice)) # between 1 & 6, starts at 1 not 0
    return rolls.sum(axis=1)

if run_sim: # check if simulation is triggered 
    progress = st.progress(0)
    all_means = [] #stores the means from each trial 
    # run trials
    for t in range(n_trials):
        results = single_experiment(n_dice, n_rolls) #runs one expirement at a time
        all_means.append(results.mean()) #stores the avg sum
        # periodically update progress
        if n_trials <= 50 or t % max(1, n_trials//50) == 0:#how often it updates, less than 50 it updates often
            progress.progress(int((t+1)/n_trials*100)) #calculates the percentage progress 
  
    df = pd.DataFrame({
        "trial": range(1, len(all_means)+1),#keeps track of num of trials 
        "mean_sum": all_means  #collects the avg result of 1 trial at a time 
        
    })
    
    string_rolls = str(n_rolls) #turn roll # to string
    string_trials = str(n_trials) #turn trial # to trial
    
    st.caption("Number of dice rolls = " + string_rolls) 
    st.caption("Number of trials = " + string_trials  ) 
    
    st.subheader("Simulation results (statistical summary)")
    st.write(df.describe().T) #statistical summary 
    
# Histogram of one representative trial (last run)
    st.subheader("Distribution of sums in the last trial")
    fig, ax = plt.subplots(figsize=(6,3.5))
    ax.hist(results, bins=np.arange(n_dice-0.5, 6*n_dice+1.5, 1), color = 'maroon')
    ax.set_xlabel("Sum of dice")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

 # Histogram of trial means
    st.subheader("Distribution of trial means (each trial averaged over rolls)")
    fig2, ax2 = plt.subplots(figsize=(6,3.5))
    ax2.hist(df["mean_sum"], bins=30, color = 'maroon')
    ax2.set_xlabel("Mean sum")
    ax2.set_ylabel("Count")
    st.pyplot(fig2)

    # Table of empirical probabilities (from last trial)
    st.subheader("Empirical probabilities (last trial)")
    probs = pd.Series(results).value_counts(normalize=True).sort_index()
    st.table(probs)


    st.info("Set parameters on the left and click **Run Monte Carlo**.")











import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

st.subtitle("Monte Carlo Simulation")

st.sidebar.header("Simulation Settings")

initial_balance = st.sidebar.number_input("Initial Account Balance ($)", value=50000)

risk_type = st.sidebar.radio("Risk Type", ["Dollar Amount", "Percent of Account"])
if risk_type == "Dollar Amount":
    risk_per_trade = st.sidebar.number_input("Risk Per Trade ($)", value=1000)
else:
    risk_pct = st.sidebar.number_input("Risk Per Trade (% of account)", value=2.0)
    risk_per_trade = initial_balance * (risk_pct / 100)

win_rate = st.sidebar.slider("Win Rate (%)", min_value=0.0, max_value=100.0, value=50.0) / 100
rr_ratio = st.sidebar.number_input("Risk-to-Reward Ratio", value=1.1)
num_trades = st.sidebar.slider("Number of Trades", 50, 1000, 500)
num_runs = st.sidebar.slider("Number of Simulated Runs", 1, 50, 20)

greys = [str(shade / 20) for shade in range(2, 10)]
np.random.seed(42)

fig, ax = plt.subplots(figsize=(10, 5))
for run in range(num_runs):
    balance = initial_balance
    history = [balance]
    for _ in range(num_trades):
        win = np.random.rand() < win_rate
        pnl = rr_ratio * risk_per_trade if win else -risk_per_trade
        balance += pnl
        history.append(balance)
    color = greys[run % len(greys)]
    ax.plot(history, color=color, linewidth=1)

ax.axhline(initial_balance, color='black', linestyle='--', label='Initial Balance')
ax.set_title("Account Balance Over Time", fontsize=14)
ax.set_xlabel("Trade Number")
ax.set_ylabel("Account Balance")
ax.grid(True)

st.pyplot(fig)


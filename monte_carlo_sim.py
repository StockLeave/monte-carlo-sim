import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit UI
st.title("Trading System Monte Carlo Simulation")

# Sidebar Inputs
initial_balance = st.number_input("Initial Account Balance ($)", value=50000)
risk_type = st.radio("Risk Type", ["Dollar Amount", "Percent of Account"])
if risk_type == "Dollar Amount":
    risk_per_trade = st.number_input("Risk Per Trade ($)", value=1000)
else:
    risk_pct = st.number_input("Risk Per Trade (% of account)", value=2.0)
    risk_per_trade = initial_balance * (risk_pct / 100)

win_rate = st.slider("Win Rate (%)", min_value=0.0, max_value=100.0, value=50.0) / 100
rr_ratio = st.number_input("Average R:R Ratio (e.g., 1.2)", value=1.1)
num_trades = st.slider("Number of Trades", 50, 1000, 500)
num_runs = st.slider("Number of Simulated Runs", 1, 50, 20)

# Simulation
st.subheader("Simulation Result")

greys = [str(shade / 20) for shade in range(2, 10)]  # dark grey tones
np.random.seed(42)

fig, ax = plt.subplots(figsize=(12, 6))
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
ax.set_title("Expected Account Balance Over Trades")
ax.set_xlabel("Trade Number")
ax.set_ylabel("Account Balance")
ax.grid(True)
st.pyplot(fig)

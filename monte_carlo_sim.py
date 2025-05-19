import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---- Style override: black & white theme ----
st.markdown("""
    <style>
        body, .stApp {
            background-color: white;
            color: black;
        }
        .block-container {
            padding: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---- App Title ----
st.title("Trading System Monte Carlo Simulation")

# ---- Inputs ----
st.sidebar.header("Simulation Settings")

initial_balance = st.sidebar.number_input("Initial Account Balance ($)", value=50000)

risk_type = st.sidebar.radio("Risk Type", ["Dollar Amount", "Percent of Account"])
if risk_type == "Dollar Amount":
    risk_per_trade = st.sidebar.number_input("Risk Per Trade ($)", value=1000)
else:
    risk_pct = st.sidebar.number_input("Risk Per Trade (% of account)", value=2.0)
    risk_per_trade = initial_balance * (risk_pct / 100)

win_rate = st.sidebar.slider("Win Rate (%)", min_value=0.0, max_value=100.0, value=50.0) / 100
rr_ratio = st.sidebar.number_input("Risk-to-Reward Ratio (e.g. 1.2 = risk $1 to make $1.20)", value=1.1)
num_trades = st.sidebar.slider("Number of Trades", 50, 1000, 500)
num_runs = st.sidebar.slider("Number of Simulated Runs", 1, 50, 20)

# ---- Simulation ----
st.subheader("Simulation Result")

greys = [str(shade / 20) for shade in range(1, 10)]  # grayscale for lines
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
ax.set_title("Expected Account Balance Over Trades", fontsize=14)
ax.set_xlabel("Trade Number")
ax.set_ylabel("Account Balance")
ax.grid(True)
st.pyplot(fig)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

st.markdown("<h2 style='text-align: center;'>Monte Carlo Simulation</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px;'>Visualize potential outcomes over time based on a probabilistic trading model.</p>", unsafe_allow_html=True)

st.sidebar.header("Simulation Settings")

initial_balance = st.sidebar.number_input("Initial Account Balance ($)", value=50000)

risk_type = st.sidebar.radio("Risk Type", ["Dollar Amount", "Percent of Account"])
if risk_type == "Dollar Amount":
    risk_per_trade = st.sidebar.number_input("Risk Per Trade ($)", value=1000)
else:
    risk_pct = st.sidebar.number_input("Risk Per Trade (% of account)", value=2.0)

win_rate = st.sidebar.slider("Win Rate (%)", min_value=0.0, max_value=100.0, value=50.0) / 100
rr_ratio = st.sidebar.number_input("Risk-to-Reward Ratio", value=1.1)
num_trades = st.sidebar.slider("Number of Trades", 50, 1000, 500)
num_runs = st.sidebar.slider("Number of Simulated Runs", 1, 50, 20)

greys = [str(shade / 20) for shade in range(2, 10)]
np.random.seed(42)

# Plot simulation
fig, ax = plt.subplots(figsize=(10, 5))
final_balances = []

for run in range(num_runs):
    balance = initial_balance
    history = [balance]
    for _ in range(num_trades):
        win = np.random.rand() < win_rate
        if risk_type == "Dollar Amount":
            trade_risk = risk_per_trade
        else:
            trade_risk = balance * (risk_pct / 100)
        pnl = rr_ratio * trade_risk if win else -trade_risk
        balance += pnl
        history.append(balance)
    color = greys[run % len(greys)]
    ax.plot(history, color=color, linewidth=1)
    final_balances.append(balance)

ax.axhline(initial_balance, color='black', linestyle='--', label='Initial Balance')
ax.set_title("Account Balance Over Time", fontsize=14)
ax.set_xlabel("Trade Number")
ax.set_ylabel("Account Balance")
ax.grid(True)

st.pyplot(fig)

# Calculate and display summary stats
avg_balance = np.mean(final_balances)
median_balance = np.median(final_balances)
max_balance = np.max(final_balances)
min_balance = np.min(final_balances)
std_dev = np.std(final_balances)
loss_probability = np.sum(np.array(final_balances) < initial_balance) / num_runs * 100

st.markdown("---")
st.markdown("### Outcome Summary")
st.markdown(f"**Average Final Balance:** ${avg_balance:,.2f}")
st.markdown(f"**Median Final Balance:** ${median_balance:,.2f}")
st.markdown(f"**Best Case (Maximum Run):** ${max_balance:,.2f}")
st.markdown(f"**Worst Case (Minimum Run):** ${min_balance:,.2f}")
st.markdown(f"**Standard Deviation:** ${std_dev:,.2f}")
st.markdown(f"**% of Runs Below Starting Balance:** {loss_probability:.1f}%")

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

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

fig, ax = plt.subplots(figsize=(10, 5))
final_balances = []
drawdowns = []

for run in range(num_runs):
    balance = initial_balance
    peak = initial_balance
    max_drawdown = 0
    history = [balance]
    
    for _ in range(num_trades):
        if risk_type == "Dollar Amount":
            trade_risk = risk_per_trade
        else:
            trade_risk = balance * (risk_pct / 100)
        win = np.random.rand() < win_rate
        pnl = rr_ratio * trade_risk if win else -trade_risk
        balance += pnl
        history.append(balance)

        if balance > peak:
            peak = balance
        dd = (peak - balance) / peak
        max_drawdown = max(max_drawdown, dd)

    final_balances.append(balance)
    drawdowns.append(max_drawdown)
    color = greys[run % len(greys)]
    ax.plot(history, color=color, linewidth=1)

ax.axhline(initial_balance, color='black', linestyle='--')
ax.set_title("Account Balance Over Time", fontsize=14)
ax.set_xlabel("Trade Number")
ax.set_ylabel("Account Balance")
ax.grid(True)

st.pyplot(fig)

avg_balance = np.mean(final_balances)
median_balance = np.median(final_balances)
max_balance = np.max(final_balances)
min_balance = np.min(final_balances)
std_dev = np.std(final_balances)
loss_probability = np.sum(np.array(final_balances) < initial_balance) / num_runs * 100

avg_drawdown = np.mean(drawdowns) * 100
max_drawdown = np.max(drawdowns) * 100
min_drawdown = np.min(drawdowns) * 100

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Final Balance**")
    st.markdown(f"Average: ${avg_balance:,.2f}")
    st.markdown(f"Median: ${median_balance:,.2f}")
    st.markdown(f"Best Case: ${max_balance:,.2f}")
    st.markdown(f"Worst Case: ${min_balance:,.2f}")

with col2:
    st.markdown("**Risk Exposure**")
    st.markdown(f"Avg Max Drawdown: {avg_drawdown:.2f}%")
    st.markdown(f"Worst Drawdown: {max_drawdown:.2f}%")
    st.markdown(f"Best Drawdown: {min_drawdown:.2f}%")
    st.markdown(f"% Below Initial Balance: {loss_probability:.1f}%")

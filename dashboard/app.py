import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px

from controller.controller import BuildingController

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Honeywell AI Building Optimizer",
    page_icon="🏢",
    layout="wide"
)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("🏢 Honeywell")

    st.markdown("---")

    st.subheader("System Status")

    st.success("🟢 Gemini AI Connected")
    st.success("🟢 EnergyPlus Ready")
    st.success("🟢 Controller Active")

    st.markdown("---")

    st.subheader("Optimization Goals")

    st.markdown("""
- Reduce HVAC Energy
- Maintain Occupant Comfort
- AI Driven Decisions
- Physics-based Validation
""")

    st.markdown("---")

    st.caption("Hackathon Demo\n\nHoneywell Building Management AI")

# ---------------- HEADER ---------------- #

st.title("🏢 Honeywell Autonomous Building Energy Optimizer")

st.markdown("""
An autonomous building management system that combines **Gemini AI** with
**EnergyPlus simulation** to optimize HVAC operation while maintaining
thermal comfort and reducing energy consumption.
""")

st.markdown("---")

# ---------------- SESSION ---------------- #

if "results" not in st.session_state:
    st.session_state.results = None

# ---------------- BUTTON ---------------- #

if st.button("🚀 Run AI Optimization", use_container_width=True):

    with st.spinner("Running AI + EnergyPlus Simulation..."):

        controller = BuildingController()
        st.session_state.results = controller.run()

results = st.session_state.results

# ==========================================================
# DISPLAY RESULTS
# ==========================================================

if results is not None:

    decision = results["decision"]
    metrics = results["results"]

    # ------------------------------------------------------

    st.header("📊 Optimization Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "HVAC Setpoint",
        f"{decision['hvac_setpoint']} °C"
    )

    col2.metric(
        "Baseline Energy",
        f"{metrics['baseline_energy']:.0f}"
    )

    col3.metric(
        "Optimized Energy",
        f"{metrics['optimized_energy']:.0f}"
    )

    saving = metrics["energy_saving_percent"]

    col4.metric(
        "Energy Saving",
        f"{saving:.2f}%"
    )

    st.markdown("---")

    # ------------------------------------------------------

    st.header("🏢 Building Health")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Temperature",
        f"{metrics['optimized_average_temp']:.2f} °C"
    )

    c2.metric(
        "Comfort Status",
        "✅ Comfortable" if metrics["comfort_maintained"] else "❌ Needs Attention"
    )

    if saving >= 0:
        c3.success("🟢 Energy Reduced")
    else:
        c3.error("🔴 Energy Increased")

    st.markdown("---")

    # ------------------------------------------------------

    left, right = st.columns([2.2, 1])

    # ================= LEFT ===================== #

    with left:

        st.subheader("🌡 Zone Temperature Comparison")

        temp_df = pd.DataFrame({
            "Zone": list(metrics["baseline_temperatures"].keys()),
            "Baseline": list(metrics["baseline_temperatures"].values()),
            "Optimized": list(metrics["optimized_temperatures"].values())
        })

        fig = px.bar(
            temp_df,
            x="Zone",
            y=["Baseline", "Optimized"],
            barmode="group",
            labels={
                "value": "Temperature (°C)",
                "variable": "Scenario"
            },
            text_auto=".1f"
        )

        fig.update_layout(height=420)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("⚡ Energy Comparison")

        energy_df = pd.DataFrame({
            "Scenario": ["Baseline", "Optimized"],
            "Energy": [
                metrics["baseline_energy"],
                metrics["optimized_energy"]
            ]
        })

        fig2 = px.bar(
            energy_df,
            x="Scenario",
            y="Energy",
            text="Energy"
        )

        fig2.update_layout(height=350)

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # ================= RIGHT ===================== #

    with right:

        st.subheader("🤖 AI Recommendation")

        st.success(
            f"Recommended HVAC Setpoint\n\n### {decision['hvac_setpoint']} °C"
        )

        if "confidence" in decision:

            st.write("Confidence")

            st.progress(float(decision["confidence"]))

            st.caption(
                f"{decision['confidence']*100:.1f}%"
            )

        st.markdown("---")

        st.subheader("AI Explanation")

        st.info(decision["reason"])

        st.markdown("---")

        st.subheader("Optimization Result")

        if metrics["comfort_maintained"]:
            st.success("✅ Comfort Maintained")
        else:
            st.error("❌ Comfort Not Maintained")

        if saving >= 0:
            st.success(
                f"Energy Reduced by {saving:.2f}%"
            )
        else:
            st.warning(
                f"Energy Increased by {abs(saving):.2f}%"
            )

    st.markdown("---")

    # ------------------------------------------------------

    st.subheader("📋 Numerical Results")

    summary = pd.DataFrame({
        "Metric": [
            "Baseline Energy",
            "Optimized Energy",
            "Average Baseline Temperature",
            "Average Optimized Temperature",
            "Energy Saving"
        ],
        "Value": [
            f"{metrics['baseline_energy']:.0f} W",
            f"{metrics['optimized_energy']:.0f} W",
            f"{metrics['baseline_average_temp']:.2f} °C",
            f"{metrics['optimized_average_temp']:.2f} °C",
            f"{metrics['energy_saving_percent']:.2f}%"
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )
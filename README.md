# 🏢 Honeywell Autonomous Building Energy Optimizer

An AI-powered Building Energy Management System (BEMS) that autonomously optimizes HVAC operation using **Google Gemini AI** and **EnergyPlus** simulations. The system analyzes building conditions, recommends energy-efficient HVAC settings, validates decisions through physics-based simulation, and presents quantitative insights through an interactive dashboard.

---

## 📌 Problem Statement

Commercial buildings consume a significant portion of global electricity, with HVAC systems accounting for nearly 40–50% of total energy usage. Traditional Building Management Systems operate on static rules and schedules, making it difficult to adapt to changing occupancy and environmental conditions.

This project demonstrates how **Generative AI** combined with **building simulation** can enable intelligent, autonomous energy optimization while maintaining occupant comfort.

---

## ✨ Features

- 🤖 AI-driven HVAC optimization using Google Gemini
- 🏢 EnergyPlus-based building simulation
- 🌡 Thermal comfort monitoring
- ⚡ Energy consumption comparison
- 📊 Interactive Streamlit dashboard
- 📈 Temperature trend visualization
- 📋 Physics-based validation of AI recommendations
- 🔄 Automated workflow from sensing to evaluation

---

# 🏗 System Architecture

```
                    ┌─────────────────────────────┐
                    │     Streamlit Dashboard     │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │     Building Controller     │
                    └──────────────┬──────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          ▼                        ▼                        ▼
  Sensor Manager          Gemini AI Agent           IDF Editor
          │                        │                        │
          └──────────────┬─────────┘                        │
                         ▼                                  │
                  AI Recommendation                         │
                         ▼                                  │
                  EnergyPlus Simulator ◄────────────────────┘
                         │
                         ▼
                 Simulation Output (CSV)
                         │
                         ▼
                     Evaluator Module
                         │
                         ▼
                 Interactive Dashboard
```

---

# ⚙ Technology Stack

## AI

- Google Gemini Flash
- Prompt Engineering

## Building Simulation

- EnergyPlus 26.1
- IDF Building Models

## Backend

- Python
- Pandas
- NumPy

## Frontend

- Streamlit
- Plotly

---

# 📂 Project Structure

```
building-ai/

│
├── agent/
│   └── llm.py
│
├── controller/
│   └── controller.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── SmallOffice.idf
│   ├── SmallOffice_modified.idf
│   └── weather.epw
│
├── energyplus/
│   ├── simulator.py
│   ├── sensor_manager.py
│   ├── idf_editor.py
│   └── evaluator.py
│
├── baseline_output/
├── optimized_output/
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Workflow

1. Read building simulation outputs.
2. Extract temperature and energy metrics.
3. Send current building state to Gemini AI.
4. Generate an optimized HVAC setpoint.
5. Modify the EnergyPlus building model.
6. Execute a new simulation.
7. Compare baseline and optimized performance.
8. Display results in the dashboard.

---

# 📊 Dashboard

The dashboard provides:

- HVAC recommendation
- Energy consumption comparison
- Temperature trends
- Occupant comfort status
- AI reasoning
- Numerical performance summary

---

# ▶ Running the Project

## 1. Clone the repository

```bash
git clone https://github.com/<username>/<repository>.git
cd building-ai
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Install EnergyPlus

Download and install **EnergyPlus 26.1**.

Update the installation path inside:

```
energyplus/simulator.py
```

Example:

```python
sys.path.insert(0, r"C:\EnergyPlusV26-1-0")
```

---

## 4. Configure Gemini API

Create a `.env` file in the project root.

```
GEMINI_API_KEY=YOUR_API_KEY
```

---

## 5. Run the dashboard

```bash
streamlit run dashboard/app.py
```

---

# 📈 Example Results

The system reports:

- Baseline Energy Consumption
- Optimized Energy Consumption
- Average Indoor Temperature
- Thermal Comfort Status
- AI HVAC Recommendation
- Energy Savings Percentage

> **Note:** Since EnergyPlus performs a physics-based simulation, optimization outcomes depend on the building model and weather conditions. The system transparently reports both improvements and trade-offs, ensuring trustworthy AI-assisted decision-making.

---

# 🔮 Future Enhancements

- Multi-zone HVAC optimization
- Occupancy-aware control
- Weather forecasting integration
- Reinforcement Learning-based optimization
- IoT sensor integration
- Real-time building deployment
- Lighting and ventilation optimization
- Historical energy analytics

---

# 👥 Team

Developed for the **Honeywell Building Automation Hackathon By Abhyuday Rastogi**.

---


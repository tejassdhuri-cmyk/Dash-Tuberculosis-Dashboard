# 🫁 Tuberculosis Dashboard

An interactive web dashboard for exploring global tuberculosis (TB) burden estimates from **1990 to 2013**, built with **Dash**, **Plotly**, and **Dash Bootstrap Components**. Pick any country or territory, choose a year range, and explore prevalence, mortality, deaths, case detection, and incidence, with a light/dark theme toggle.

## ✨ Features

- **Country picker**: 219 countries and territories (defaults to India)
- **Year range selector**: choose start and end years between 1990 and 2013
- **Five tabs of visualisations:**

  | Tab | What it shows |
  |---|---|
  | **TB Prevalence** | Bar chart of estimated TB prevalence (colored by estimation method) and an **animated world choropleth map** across years |
  | **Estimated Mortality** | TB mortality per 100,000 population, HIV-negative and HIV-positive side by side |
  | **Estimated Deaths** | Estimated number of TB deaths, excluding HIV and among HIV-positive people |
  | **Case Detection** | Case detection rate (all forms), in percent |
  | **TB Incidence** | Estimated number of incident TB cases (all forms), colored by estimation method |

- **Light / dark theme switch** (Bootstrap and Darkly) that restyles every chart
- Responsive layout: charts stack on small screens

## 🗂️ Dataset

| File | Description |
|---|---|
| `data/TB_Burden_Country.csv` | 5,120 rows × 47 columns: yearly TB burden estimates per country (1990–2013), including population, prevalence, mortality, deaths, incidence, HIV co-infection, and case detection, each with low/high bounds and the estimation method |
| `data/Countries by continents.csv` | Country-to-continent mapping, merged with the TB data on country name for the choropleth map |

Key columns used by the dashboard include `Country or territory name`, `ISO 3-character country/territory code`, `Year`, `Estimated prevalence of TB (all forms)`, `Estimated number of deaths from TB (all forms, excluding HIV)`, `Estimated number of incident cases (all forms)`, and `Case detection rate (all forms), percent`.

## 🛠️ Tech Stack

- [Dash](https://dash.plotly.com/) for the web app framework and callbacks
- [Plotly Express](https://plotly.com/python/plotly-express/) for charts and maps
- [dash-bootstrap-components](https://dash-bootstrap-components.opensource.faculty.ai/) and [dash-bootstrap-templates](https://github.com/AnnMarieW/dash-bootstrap-templates) for layout and theme switching
- [pandas](https://pandas.pydata.org/) and NumPy for data handling
- [joblib](https://joblib.readthedocs.io/) for loading a pre-trained regression model

## 📁 Project Structure

```
.
├── tb_dashboard.py             # Dash app (layout + callbacks)  
├── data/
│   ├── TB_Burden_Country.csv
│   └── Countries by continents.csv
├── requirements.txt
└── README.md
```


## 🚀 Getting Started

### Prerequisites

- Python 3.9+

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Run the app

```bash
python tb_dashboard.py
```

Then open **http://127.0.0.1:8050** in your browser.

## 📦 requirements.txt

```
dash
dash-bootstrap-components
dash-bootstrap-templates
plotly
pandas
numpy


## 🧭 How It Works

1. `TB_Burden_Country.csv` is loaded and merged with the continents file on country name.
2. A single Dash callback listens to the country dropdown, the start and end year dropdowns, and the theme switch.
3. On every change it filters the data, rebuilds all eight figures, and applies the `plotly` (light) or `plotly_dark` template.

## 🔮 Possible Improvements

- Add confidence-interval bands using the low/high bound columns
- Validate that the start year is not later than the end year
- Add continent- or region-level filters and comparisons across countries
- Deploy to Render, Railway, or Hugging Face Spaces

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

## 🙏 Acknowledgements

- TB burden estimates in the World Health Organization's global TB data format
- The Plotly Dash community for excellent documentation and examples

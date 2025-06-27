# 📦 Dryfit

**Dryfit** is a research-based desktop appliciation developed to analyze moisture ratio history data from the dehydration of agro-products. It offers tools to fit several thin-layer drying models to M.R history data, evaluates the goodness of fit of each model, moisture diffusivity computation, and visualization amongst many others to support post-harvest technology and food processing research.

---

## 🗂 Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Screenshots](#screenshots)  
- [Models Supported](#models-supported)  
- [Project Structure](#project-structure)  
- [Contributing](#contributing)  
- [License](#license)  
- [Acknowledgements](#acknowledgements)

---
## 💻 System Requirements
- **Operating System:** Windows 7 or higher  
- **Python:** 3.13.0 or later  
- **Dependencies:**
  - numpy  
  - pandas  
  - scipy  
  - matplotlib  
  - customtkinter  
  - openpyxl
---

## ✨ Features

- Load and analyze moisture ratio history data from Excel file
- Calculate moisture diffusivity.
- Calculate thermodynamic properties (Enthalpy, Entropy and Gibbs Free Energy) 
- Fit multiple thin-layer drying models using Non-linear regression (e.g., Page, Henderson and Pabis, Logarithmic).    
- Calculate statistical parameters (R², RMSE, SSE).
- Use the statictical parameters to determine the best model.
- Use the best model to predict moisture ratio from time.
- Generate data for drying, drying rate and krischer plots.
- Create visual plots of the data generated.
- Export analysis results and plots.  
- User-friendly GUI (Tkinter & CustomTkinter).

---

## ⚙️ Installation

> Requires Python 3.13.0 or later

```bash
git clone https://github.com/mazi-kunle/DRYING-SOFTWARE.git
cd DRYING-SOFTWARE
pip install -r requirements.txt
python app.py
```
---
## 📂 Data Format

- **Input data:** DryFit only accepts excel files (`.xlsx`) with the following structure.
- **Output data:** Results are stored in a folder which includes an excel file containing the calculated data in several sheets and the required plots in `jpeg` format.

| Temperature (Celcius)| Thickness (mm)| Time (min) | Moisture Ratio |
|----------------------|---------------|------------|----------------|
| 60                   | 1.5           | 0          | 1.000          |
|                      |               | 10         | 0.850          |
|                      |               | 20         | 0.700          |
|                      |               | ...        | ...            |

**Requirements:**
- Each dataset for a particular experiment should be placed in several sheets in one excel file.
- The excel sheet must contain only 4 columns.
- The first column must contain only one temperature value in degree Celcius.
- The second column must contain only one thickness value in mm
- The third column can have several time values in minutes
- The last column can have several M.R values (Dry Basis).
  
---

## 🚀 Usage

*Add usage instructions here.*

From the GUI:
1. Click to upload your Excel drying data file.  
2. Select the model(s) to fit.  
3. Click **Analyze**.  
4. View plots, parameters, and statistics.  
5. Export results as needed.

---

## 🖼 Screenshots

_Add screenshots of the GUI interface, model plots, or output tables here._

---

## 📊 Models Supported

- Newton Model  
- Page Model  
- Henderson and Pabis Model  
- Logarithmic Model  
- Midilli et al. Model  
- Two-term exponential model  

---

## 🧾 Project Structure


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
- **Python (for developers):** 3.13.0 or later  
- **Dependencies (for developers):**
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

DryFit can be run in two ways:
### 🔹 Option 1: Using Python (for developers or researchers with Python installed)
1. **Clone the repository:**
  ```bash
  git clone https://github.com/mazi-kunle/DRYING-SOFTWARE.git
  cd DRYING-SOFTWARE
  ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
  ```bash
  python app.py
  ```
### 🔹 Option 2: Windows Executable Installation (for End Users)

DryFit can be installed like a regular Windows desktop application — **no need to install Python or run any scripts**.

#### 🧾 Steps:

1. Download the installer from the [Releases](https://github.com/yourusername/dryfit/releases) page  
   (e.g., `DryFit_Setup.exe`).
2. Double-click the downloaded file to run the installer.
3. Follow the on-screen instructions to complete installation.
4. After installation:
   - Launch the app from the **Start Menu**
   - Or use the **Desktop shortcut** (if selected during setup)

✅ **Note:** This version is built using [PyInstaller](https://www.pyinstaller.org/) and includes all required dependencies bundled within the executable.

#### 💡 System Requirements:

- **Operating System:** Windows 10 or higher (64-bit)
- **Disk Space:** ~100MB (depends on packaging)
- **Permissions:** Administrator access may be required for installation

> This option is recommended for non-technical users or when sharing the app with field researchers and practitioners.

---
## 📂 Data Format

**Input data:** DryFit only accepts excel files (`.xlsx`) with the following structure.
  
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

**Output data:** Results are stored in a folder which includes an excel file containing the calculated data in several sheets and the required plots in `jpeg` format.

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


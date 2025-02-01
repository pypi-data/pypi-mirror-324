
# PyDataLens

PyDataLens is a Python package designed to streamline the process of **Exploratory Data Analysis (EDA)**, **data cleaning**, and **visualization**. 
It enables data scientists and analysts to quickly prepare, explore, and gain insights from datasets with minimal effort.

---

## Features

### 1. **Smart Summarization**
- Automatically generates a summary of the dataset, including:
  - Data types
  - Missing values
  - Descriptive statistics
  - Unique value counts

### 2. **Data Cleaning**
- Detects and handles missing values using various strategies (mean, median, mode).
- Identifies and removes duplicate rows.
- Supports basic outlier detection (planned for future updates).

### 3. **Correlation Analysis**
- Generates a correlation matrix to identify relationships between features.
- Provides heatmaps for better visualization.

### 4. **Automatic Visualizations**
- Supports generating:
  - Histograms
  - Box plots
  - Correlation heatmaps
  - Scatter plots (planned for future updates).

### 5. **Report Generation**
- Exports EDA results and visualizations into a detailed **HTML report** for easy sharing.

---

## Installation

### Using pip (from source)
1. Clone the repository:
   ```bash
   git clone https://github.com/gopalakrishnanarjun/PyDataLens.git
   cd PyDataLens
   ```
2. Install the package:
   ```bash
   pip install -e .
   ```

### Dependencies
- Python >= 3.6
- pandas >= 1.0
- numpy >= 1.18
- matplotlib >= 3.1
- seaborn >= 0.11

Install dependencies manually:
```bash
pip install pandas numpy matplotlib seaborn
```

---

## Quick Start

### 1. Import the package
```python
from pydatalens import eda, cleaning, visualizations
```

### 2. Load a dataset
```python
import pandas as pd
df = pd.read_csv("your_dataset.csv")
```

### 3. Summarize the dataset
```python
print(eda.summarize(df))
```

### 4. Handle missing values
```python
df_cleaned = cleaning.handle_missing(df, strategy="mean")
```

### 5. Visualize the data
```python
visualizations.plot_histogram(df_cleaned, column="age")
visualizations.correlation_heatmap(df_cleaned)
```

---

## Examples

### Summarizing the Data
```python
from pydatalens import eda
summary = eda.summarize(df)
print(summary)
```

### Cleaning the Data
```python
from pydatalens import cleaning
df = cleaning.handle_missing(df, strategy="median")
df = cleaning.drop_duplicates(df)
```

### Visualizing the Data
```python
from pydatalens import visualizations
visualizations.plot_histogram(df, "column_name")
visualizations.correlation_heatmap(df)
```

---

## Future Enhancements
- Advanced anomaly detection.
- Support for time series analysis.
- Enhanced visualization options (e.g., scatter plots, pair plots).
- Integration with machine learning pipelines.

---

## Contributing
Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

---

## License
PyDataLens is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Support
For any questions or issues, please feel free to open an issue on GitHub.

---

**Author:** Gopalakrishnan Arjunan 
**GitHub:** [gopalakrishnanarjun](https://github.com/gopalakrishnanarjun)

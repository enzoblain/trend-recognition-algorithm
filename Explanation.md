# Trend Recognition Algorithm

The Trend Recognition Algorithm processes financial data to identify market trends, classifying each time period as Bullish or Bearish. The process is divided into two main phases: **Data Preparation** and **Algorithm Workflow**.

## 1. Data Preparation

### 1.1. Input Validation
- **Objective**: Ensure the input data is suitable for analysis.
- **Process**:
  - The algorithm checks if the input is either a dictionary or a Pandas DataFrame.
  - If the input is a dictionary, it is converted into a DataFrame.
  - If the input is neither a dictionary nor a DataFrame, an error is raised.

### 1.2. Column Verification
- **Objective**: Confirm the presence of all necessary columns in the DataFrame.
- **Process**:
  - The algorithm checks for five essential columns: `datetime`, `high`, `open`, `close`, and `low`.
  - If any of these columns are missing, an error is raised, halting further processing.

### 1.3. Handling Missing Data
- **Objective**: Ensure the data is complete and ready for analysis.
- **Process**:
  - The algorithm calculates the proportion of missing data in the DataFrame.
  - If the proportion of missing data exceeds 20%, a warning is issued to indicate potential issues with the analysis.
  - Rows with missing data are dropped to ensure a clean dataset.

### 1.4. Initial Trend Classification
- **Objective**: Categorize each time period as Bullish or Bearish.
- **Process**:
  - For each row in the DataFrame, the algorithm compares the `open` and `close` prices.
  - If the `close` price is higher than the `open`, the period is classified as Bullish.
  - If the `close` price is lower than the `open`, it is classified as Bearish.

## 2. Algorithm Workflow

### 2.1. Initialize First Trend
- **Objective**: Set up the initial trend based on the first data point.
- **Process**:
  - The first time period (candle) is used to define the initial trend.
  - The algorithm records the trend type (Bullish or Bearish), high and low prices, retest level, and start time.

### 2.2. Identify Sub-Trends
- **Objective**: Track changes within the main trend to detect sub-trends.
- **Process**:
  - As the algorithm iterates through the data, it monitors for deviations within the main trend.
  - If a sub-trend begins, it records the new high, low, and retest levels for that period.

### 2.3. Trend Confirmation and Transition
- **Objective**: Confirm trend continuation or transition to a new trend.
- **Process**:
  - The algorithm checks if the current trend continues or if a new trend emerges based on price movements and thresholds.
  - If a new trend is identified, the current trend is closed and saved, and the new trend is initialized.

### 2.4. Finalize Trends
- **Objective**: Conclude the trend analysis.
- **Process**:
  - After processing all data points, the algorithm finalizes any ongoing trends.
  - The identified trends are then stored for further analysis or use.

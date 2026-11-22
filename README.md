# IHSG Data Ingestion CI/CD Pipeline

Automated financial data ingestion pipeline for the Jakarta Composite Index (IHSG) and selected global financial instruments using Python, GitHub Actions, and Microsoft Azure Blob Storage.

## Overview

This project implements an automated data ingestion pipeline to collect historical financial market data from Yahoo Finance, validate and consolidate the collected data, and store the results in Azure Blob Storage.

The pipeline is designed with Continuous Integration (CI) and Continuous Deployment (CD) workflows using GitHub Actions. It supports automated execution every six hours as well as manual execution through GitHub Actions.

The main objective is to establish a reliable and reproducible data ingestion process that integrates external financial data sources with cloud-based storage.

## Project Objectives

- Automate financial data collection from Yahoo Finance.
- Retrieve historical data for IHSG and selected global financial instruments.
- Validate data quality before storage.
- Consolidate and remove duplicate records.
- Automate data ingestion using GitHub Actions.
- Implement CI testing to maintain code reliability.
- Store the resulting dataset in Microsoft Azure Blob Storage.
- Schedule automated pipeline execution every six hours.

## System Architecture

The pipeline consists of the following components:

```text
Yahoo Finance
     |
     v
Python Data Ingestion
     |
     v
Data Processing
     |
     v
Data Validation
     |
     v
CSV Generation
     |
     v
Azure Blob Storage

GitHub Repository
     |
     v
GitHub Actions
     |
     +---- Continuous Integration (CI)
     |
     +---- Continuous Deployment (CD)
                  |
                  v
             Azure Login
             (OIDC Authentication)
                  |
                  v
             Run Ingestion
```

### Pipeline Workflow

1. GitHub Actions is triggered by a push, pull request, scheduled execution, or manual workflow dispatch, depending on the configured workflow.
2. The Python environment and project dependencies are prepared.
3. GitHub Actions authenticates with Microsoft Azure using OpenID Connect (OIDC).
4. The ingestion script retrieves financial data from Yahoo Finance.
5. The collected data is consolidated and checked through validation rules.
6. The resulting dataset is saved as a CSV file.
7. The CSV file is uploaded to Azure Blob Storage.

## Data Sources

Financial data is retrieved from Yahoo Finance using the `yfinance` Python library.

The pipeline collects data from eight financial instruments:

| Ticker | Instrument | Description |
|---|---|---|
| `^JKSE` | JKSE | Jakarta Composite Index (IHSG) |
| `CL=F` | CLF | WTI Crude Oil Futures |
| `GC=F` | GCF | Gold Futures |
| `IDR=X` | IDRX | USD/IDR Exchange Rate |
| `^DJI` | DJI | Dow Jones Industrial Average |
| `^HSI` | HSI | Hang Seng Index |
| `^N225` | N225 | Nikkei 225 |
| `EEM` | EEM | Emerging Markets ETF |

**Historical data period:** Starting from January 1, 2018, subject to data availability from Yahoo Finance.

### Dataset Structure

The consolidated dataset contains the following columns:

| Column | Description |
|---|---|
| Date | Trading date |
| Open | Opening price |
| High | Highest price |
| Low | Lowest price |
| Close | Closing price |
| Adj Close | Adjusted closing price |
| Volume | Trading volume |
| Ticker | Yahoo Finance ticker symbol |
| Instrument | Instrument identifier |

## Data Processing and Validation

The ingestion process performs several operations before uploading the dataset:

1. **Data Collection:** Retrieves historical financial data for each configured ticker.
2. **Data Consolidation:** Combines the collected data into a single DataFrame.
3. **Date Formatting:** Standardizes the date format to `YYYY-MM-DD`.
4. **Duplicate Removal:** Removes duplicate records based on `Date` and `Ticker`, keeping the latest record.
5. **Data Sorting:** Sorts records by date and ticker.
6. **Data Validation:** Checks required columns, expected tickers, date validity, duplicate records, numeric values, and OHLC consistency.
7. **CSV Generation:** Saves the consolidated dataset as `ihsg_historical.csv`.
8. **Cloud Upload:** Uploads the generated CSV file to Azure Blob Storage.

## CI/CD Implementation

GitHub Actions is used to automate testing and data ingestion.

### Continuous Integration (CI)

The CI workflow is configured in:

`.github/workflows/ci.yml`

The CI process includes:

- Checking out the repository.
- Setting up Python 3.10.
- Installing project dependencies.
- Running automated unit tests using pytest.

The workflow is triggered by:
- Push events to the `main` and `feature/ihsg-ingestion` branches.
- Pull requests targeting the `main` branch.

### Continuous Deployment (CD)

The CD workflow is configured in:

`.github/workflows/ingestion.yml`

The CD process automates the execution of the data ingestion script and uploads the generated dataset to Azure Blob Storage.

**Execution triggers:**

| Trigger | Configuration | Description |
|---|---|---|
| Scheduled | `0 */6 * * *` | Automatically runs every six hours |
| Manual | `workflow_dispatch` | Allows manual execution through GitHub Actions |

The scheduled workflow uses UTC time. In Western Indonesia Time (WIB), the intended schedule is 01:00, 07:00, 13:00, and 19:00.

## Microsoft Azure Integration

The project uses Azure Blob Storage as its cloud storage destination.

### Storage Configuration

| Component | Configuration |
|---|---|
| Resource Group | `rg-ihsg-cicd` |
| Storage Account | `stihsgcicd` |
| Container | `ihsg-data` |
| Output File | `ihsg_historical.csv` |
| Authentication | Microsoft Entra ID with OIDC |

### Authentication

GitHub Actions authenticates with Azure using OpenID Connect (OIDC) through the `azure/login@v2` action.

This approach uses Microsoft Entra ID federated credentials, allowing GitHub Actions to access Azure resources without storing long-lived Azure credentials in the repository.

The application is assigned the `Storage Blob Data Contributor` role to allow it to upload data to the configured storage account.

### Storage Process

The ingestion script uses the Azure SDK for Python:

- `azure-identity` for authentication.
- `azure-storage-blob` for Blob Storage operations.

The output file is uploaded to the `ihsg-data` container with the blob name `ihsg_historical.csv`. Existing files are overwritten with the latest consolidated dataset.

## Repository Structure

```text
ihsg-cicd-pipeline/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── ingestion.yml
│
├── src/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── validation.py
│   └── storage.py
│
├── tests/
│   └── test_ingestion.py
│
├── data/
│   └── .gitkeep
│
├── requirements.txt
├── .gitignore
└── README.md
```

### Main Components

| File | Responsibility |
|---|---|
| `src/ingestion.py` | Retrieves, consolidates, validates, and saves financial data before uploading it to Azure |
| `src/validation.py` | Defines data validation rules |
| `src/storage.py` | Handles authentication and file uploads to Azure Blob Storage |
| `tests/test_ingestion.py` | Contains automated unit tests |
| `.github/workflows/ci.yml` | Defines the Continuous Integration workflow |
| `.github/workflows/ingestion.yml` | Defines the scheduled and manually triggered ingestion workflow |
| `requirements.txt` | Lists Python project dependencies |

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.10 | Main programming language |
| yfinance | Financial data retrieval |
| Pandas | Data processing and manipulation |
| Pytest | Automated testing |
| Git & GitHub | Version control and collaboration |
| GitHub Actions | CI/CD automation and scheduling |
| Microsoft Entra ID | Identity and authentication |
| Azure Identity | Azure authentication SDK |
| Azure Blob Storage | Cloud data storage |

## Setup and Installation

### Prerequisites

Make sure the following tools are available:

- Python 3.10 or later
- Git
- A GitHub account
- An Azure subscription
- An Azure Storage Account

### 1. Clone the Repository

```bash
git clone https://github.com/yoekesekti/ihsg-cicd-pipeline.git
cd ihsg-cicd-pipeline
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows:

```cmd
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Azure Authentication

Set the storage account environment variable:

```cmd
set AZURE_STORAGE_ACCOUNT=stihsgcicd
```

For local execution, authenticate using Azure CLI:

```bash
az login
```

Ensure that the authenticated identity has the `Storage Blob Data Contributor` role on the target storage account.

For GitHub Actions, configure the following repository variables under **Settings → Secrets and variables → Actions → Variables**:

| Variable | Description |
|---|---|
| `AZURE_CLIENT_ID` | Application (client) ID |
| `AZURE_TENANT_ID` | Directory (tenant) ID |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID |
| `AZURE_STORAGE_ACCOUNT` | Storage account name |

Also configure a federated credential in Microsoft Entra ID for the GitHub repository and the `main` branch.

### 5. Run the Ingestion Pipeline

```bash
python -m src.ingestion
```

The script retrieves the financial data, validates it, generates the CSV file, and uploads the result to Azure Blob Storage.

### 6. Run Unit Tests

```bash
python -m pytest tests/ -v
```

## Execution Results

The initial successful GitHub Actions CD execution produced the following results:

| Metric | Result |
|---|---:|
| Number of instruments | 8 |
| Total records | 17,758 |
| Output format | CSV |
| Output filename | `ihsg_historical.csv` |
| Data validation | Successful |
| Azure Blob upload | Successful |

The execution log confirmed:

```text
Validasi data berhasil.
Total baris: 17758
Jumlah instrumen: 8
Total data: 17758 baris
File tersimpan: data/ihsg_historical.csv

Upload ke Azure Blob Storage berhasil.
Container: ihsg-data
Blob: ihsg_historical.csv
```

The generated CSV file was successfully stored in the `ihsg-data` container of the Azure Storage Account.

## Project Limitations

- Data availability depends on Yahoo Finance.
- Financial market data is subject to trading schedules and source updates.
- The six-hour schedule does not guarantee that new market data will be available at every execution.
- GitHub Actions scheduled workflows may experience execution delays.
- The pipeline currently stores the consolidated dataset as a single CSV file in Azure Blob Storage.

## Future Improvements

Potential improvements include:

- Adding more comprehensive data quality checks.
- Implementing automated failure notifications.
- Adding ingestion logs and monitoring.
- Improving retry mechanisms for temporary API failures.
- Expanding the financial instrument coverage.
- Integrating the stored dataset with downstream analytics and forecasting workflows.

## Author

**Yoeke Sekti Pertiwi**

GitHub: [@yoekesekti](https://github.com/yoekesekti)

---

*This project was developed as part of a Cloud Computing coursework assignment to implement data ingestion automation, CI/CD workflows, and cloud-based data storage.*

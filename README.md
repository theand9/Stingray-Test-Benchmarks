# **Stingray Test Benchmarks**

## **Overview**
Stingray Test Benchmarks is a Command Line Interface (CLI) utility designed to benchmark various functions of the [Stingray](https://github.com/StingraySoftware/stingray) library. It facilitates performance testing and stores results in a structured format for visualization.

---

## **Features**
- **Benchmarking**: Evaluate the performance of Stingray functions.
- **Data Storage**: Results are saved in the `data` directory with timestamps and commit messages for version control.
- **Visualization**: Generate interactive plots using Plotly to analyze benchmark results.

---

## **Project Structure**
```
stingray-Test-Benchmarks/
├── code/                   # CLI utility source code
├── data/                   # Directory to store benchmark results
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
└── requirements.json       # Project dependencies
```

---

## **Setup and Installation**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/theand9/stingray-Test-Benchmarks.git
   cd stingray-Test-Benchmarks
   ```

2. **Install Dependencies**
   - Ensure you have Python installed.
   - Install required packages:
     ```bash
     pip install -r requirements.json
     ```

3. **Directory Structure**
   - Ensure the `data` directory exists in the main project folder to store benchmark results.

---

## **Usage**

1. **Run Benchmarks**
   - Execute the CLI utility to benchmark Stingray functions:
     ```bash
     python code/Main_Bench.py
     ```
   - Follow the on-screen prompts to select functions and input parameters.

2. **View Results**
   - Benchmark results are saved in the `data` directory with timestamps.
   - Use Plotly to visualize the results (TO-DO):
     ```bash
     python code/visualize_results.py
     ```

---

## **Notes**
- A web-hosted version of this utility is planned; the link will be provided upon release.
- Ensure the `data` directory is in the same main folder as the code to store results properly.

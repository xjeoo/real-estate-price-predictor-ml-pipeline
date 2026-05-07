# Real Estate Price AI Predictor - ML Pipeline

## Work in Progress
**Current Focus: Data Acquisition Phase**

This repository serves as the core Machine Learning engine for a property price prediction system. It is designed to handle the heavy-lifting of the data lifecycle, from raw web harvesting to model persistence.

### Project Scope
This specific component of the ecosystem is dedicated to:
1. **Automated Data Acquisition**: Scalable harvesting of real estate listings to build a robust dataset.
2. **Data Cleaning and Preprocessing**: Transformation of raw, unstructured HTML-extracted data into a clean, feature-engineered format suitable for machine learning.
3. **Model Training and Evaluation**: Implementing and tuning a Random Forest Regressor to capture complex market trends and estimate property values.

### Pipeline Architecture
The system is built as a sequential pipeline to ensure data integrity and reproducibility:

*   **Phase 1: Harvesting (Done)**: Extracting relevant features over 25k listings.
*   **Phase 2: Cleaning (Starting)**: Handling missing values, outlier detection, and encoding categorical variables.
*   **Phase 3: Training (Planned)**: Model selection, hyperparameter tuning, and validation.

### Current Implementation Details
The system is currently in the **Data Acquisition** stage. The harvester is implemented with focus on:
*   Robust error handling and session resilience.
*   Smart rate-limiting to ensure respectful crawling.
*   Incremental saving (Append-mode) to protect progress during long-running tasks.

---
*Note: This repository is part of a larger architecture. Once the pipeline is finalized, the trained model will be exposed via a dedicated API for real-time predictions.*

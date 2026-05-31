# Real Estate Price AI Predictor - ML Pipeline

## Work in Progress
**Current Focus: Model Training**

This repository serves as the core Machine Learning engine for a property price prediction system. It is designed to handle the heavy lifting of the data lifecycle, from raw web harvesting to model persistence.

### Project Scope
This specific component of the ecosystem is dedicated to:
1. **Automated Data Acquisition**: Scalable harvesting of 27k+ real estate listings to build a robust dataset.
2. **Data Cleaning and Preprocessing**: Transformation of raw, unstructured HTML-extracted data into a clean, feature-engineered format.
3. **Model Training and Evaluation**: Implementing and tuning a Random Forest Regressor to capture market trends.

### Pipeline Architecture
The system is built as a sequential pipeline:

* **Phase 1: Harvesting (Done)**: Extracting relevant features over 27k listings.
    * *Features extracted:* `listing_id`, `price`, `currency`, `tva_included`, `sector`, `neighbourhood`, `distance_to_subway_meters`, `nr_of_rooms`, `usable_surface_sq_meters`, `floor`, `max_floor`, `construction year`, `construction_status`, `layout`, `number_of_bathrooms`, `comfort_grade`, `has_balcony`, `parking_spots`, `heating_type`, `url`.
* **Phase 2: Cleaning (Done)**: Handling missing values, outlier detection, and encoding categorical variables.
* **Phase 3: Training (Starting)**: Model selection, hyperparameter tuning, and validation.

### Current Implementation Details
The system has completed the **Data Cleaning** stage and is moving into **Model Training**.

#### **1. Data acquisition is done.** The harvester is implemented with focus on:
* **Session Management**: Using `requests.Session` and rotating User-Agents for resilience.
* **Anti-Throttling**: Smart rate limiting and session rotation (every 150 requests).
* **Data Integrity**: Advanced parsing logic tailored to handle complex edge cases and ensure high quality data extraction.
* **Persistence**: Incremental saving (Append mode) and Resume logic to protect progress.

#### **2. Data cleaning is done.** The preprocessing pipeline is implemented with focus on:
* **Deduplication**: Removed phantom listings caused by platform redirects based on exact macro-feature matching.
* **Financial Standardization**: Converted all currencies to Euro and dynamically integrated missing VAT (5% or 19%) based on legal thresholds to reflect actual out-of-pocket costs.
* **Domain-Specific Imputation**: 
  * Handled missing bathrooms by room count medians.
  * Imputed `max_floor` and `construction year` using sector medians. 
  * Defaulted missing subway distances to `3500m` and empty parking spots to `0`.
* **Feature Engineering**: Created `floor_ratio` (`floor` / `max_floor`) and `construction_age` features to better capture value depreciation.
* **Outlier Management**: Clamped excessive parking spot numbers (max `8`) and strictly filtered physical/temporal impossibilities (surfaces < 15 sqm or > 350 sqm; impossible construction ages).
* **Encoding & Formatting**: Applied One-Hot Encoding to categorical features (mapping `NaNs` as "Unknown") and dropped irrelevant textual columns (`neighbourhood`, `url`, `listing_id`). The final output is a 100% numerical/boolean feature matrix.

---
*Note: This repository is part of a larger architecture. Once the pipeline is finalized, the trained model will be exposed via a dedicated API for real-time predictions.*
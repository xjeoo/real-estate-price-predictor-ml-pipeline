# Real Estate Price AI Predictor - ML Pipeline

## Work in Progress
**Current Focus: Data Cleaning**

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
* **Phase 2: Cleaning (Starting)**: Handling missing values, outlier detection, and encoding categorical variables.
* **Phase 3: Training (Planned)**: Model selection, hyperparameter tuning, and validation.

### Current Implementation Details
The system is currently in the **Data Cleaning** stage.
#### **Data acquisition is done.** The harvester is implemented with focus on:
* **Session Management**: Using `requests.Session` and rotating User-Agents for resilience.
* **Anti-Throttling**: Smart rate limiting and session rotation (every 150 requests).
* **Data Integrity**: Advanced parsing logic tailored to handle complex edge cases and ensure high quality data extraction.
* **Persistence**: Incremental saving (Append mode) and Resume logic to protect progress.

---
*Note: This repository is part of a larger architecture. Once the pipeline is finalized, the trained model will be exposed via a dedicated API for real-time predictions.*
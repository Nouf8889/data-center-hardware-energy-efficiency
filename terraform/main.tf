terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = "data-center-hardware"
  region  = "europe-west1"
}

# Existing BigQuery dataset: raw_data
resource "google_bigquery_dataset" "raw_data" {
  dataset_id = "raw_data"
  project    = "data-center-hardware"
  location   = "EU"
}

# Existing BigQuery dataset: analytics
resource "google_bigquery_dataset" "analytics" {
  dataset_id = "analytics"
  project    = "data-center-hardware"
  location   = "EU"
}

from google.cloud import bigquery

def create_bigquery_client():
    """Creates a BigQuery client."""
    client = bigquery.Client()
    return client

def list_datasets(client):
    """Lists datasets in the BigQuery project."""
    datasets = list(client.list_datasets())
    if datasets:
        print("Datasets in project:")
        
        for dataset in datasets:
            print(f"- {dataset.dataset_id}")
    else:
        print("No datasets found.")

if __name__ == "__main__":
    client = create_bigquery_client()
    list_datasets(client)

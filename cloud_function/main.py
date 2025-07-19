import os
import pandas as pd
from datetime import datetime
from neo4j import GraphDatabase

def process_carbon_data(request):
    """
    Reads mock data from GCS, transforms it, and loads it into a Neo4j graph.
    """
    try:
        # --- 1. CONFIGURATION (Loaded from Environment Variables) ---
        bucket_name = os.environ.get('GCS_BUCKET_NAME')
        neo4j_uri = os.environ.get('NEO4J_URI')
        neo4j_user = os.environ.get('NEO4J_USER')
        # This now gets the actual password, injected by Cloud Run from Secret Manager
        neo4j_password = os.environ.get('NEO4J_PASSWORD')
        
        gcp_file_name = 'mock_gcp_footprint.csv'
        aws_file_name = 'mock_aws_footprint.csv'

        # --- 2. EXTRACT ---
        print(f"Extracting data from bucket: {bucket_name}...")
        gcp_uri = f'gs://{bucket_name}/{gcp_file_name}'
        aws_uri = f'gs://{bucket_name}/{aws_file_name}'
        gcp_df = pd.read_csv(gcp_uri)
        aws_df = pd.read_csv(aws_uri)
        print("Extraction successful.")

        # --- 3. TRANSFORM ---
        print("Transforming data...")
        # (Transformation logic is the same)
        aws_transformed = aws_df.copy(); aws_transformed['cloud_provider'] = 'AWS'; aws_transformed['account_id'] = aws_transformed['aws_account_id'].astype(str); aws_transformed['region'] = aws_transformed['aws_region']; aws_transformed['service'] = aws_transformed['service']; aws_transformed['scope1_emissions'] = aws_transformed['emissions_scope_1']; aws_transformed['scope2_emissions'] = aws_transformed['emissions_scope_2_market_based']; aws_transformed['scope3_emissions'] = 0.0; aws_transformed['year'] = pd.to_datetime(aws_transformed['billing_period']).dt.year; aws_transformed['month'] = pd.to_datetime(aws_transformed['billing_period']).dt.month; aws_transformed['day'] = 1
        aws_final = aws_transformed[['cloud_provider', 'account_id', 'region', 'service', 'scope1_emissions', 'scope2_emissions', 'scope3_emissions', 'year', 'month', 'day']]
        gcp_transformed = gcp_df.copy(); gcp_transformed['cloud_provider'] = 'GCP'; gcp_transformed['account_id'] = gcp_transformed['project.id']; gcp_transformed['region'] = gcp_transformed['location.region']; gcp_transformed['service'] = gcp_transformed['service.description']; gcp_transformed['scope1_emissions'] = gcp_transformed['carbon_footprint_kgco2e.scope1']; gcp_transformed['scope2_emissions'] = gcp_transformed['carbon_footprint_kgco2e.scope2_market_based']; gcp_transformed['scope3_emissions'] = gcp_transformed['carbon_footprint_kgco2e.scope3']; gcp_transformed['year'] = gcp_transformed['usage_date.year']; gcp_transformed['month'] = gcp_transformed['usage_date.month']; gcp_transformed['day'] = gcp_transformed['usage_date.day']
        gcp_final = gcp_transformed[['cloud_provider', 'account_id', 'region', 'service', 'scope1_emissions', 'scope2_emissions', 'scope3_emissions', 'year', 'month', 'day']]
        combined_df = pd.concat([aws_final, gcp_final], ignore_index=True); combined_df['created_at'] = datetime.now().isoformat()
        print(f"Transformation successful.")

        # --- 4. LOAD ---
        print("Loading data into Neo4j...")
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        with driver.session() as session:
            for index, row in combined_df.iterrows():
                session.run("""
                    MERGE (c:Company {name: 'PaySydney Pty Ltd'})
                    MERGE (cp:CloudProvider {name: $provider})
                    MERGE (p:Project {id: $account_id, provider: $provider})
                    MERGE (cr:CarbonReport {service: $service, region: $region, year: $year, month: $month})
                    SET cr.scope1 = $s1, cr.scope2 = $s2, cr.scope3 = $s3, cr.loaded_at = $created_at
                    MERGE (c)-[:USES_PROVIDER]->(cp)
                    MERGE (cp)-[:HAS_PROJECT]->(p)
                    MERGE (p)-[:GENERATED]->(cr)
                """, {
                    "provider": row['cloud_provider'], "account_id": str(row['account_id']), "service": row['service'],
                    "region": row['region'], "year": int(row['year']), "month": int(row['month']),
                    "s1": float(row['scope1_emissions']), "s2": float(row['scope2_emissions']), "s3": float(row['scope3_emissions']),
                    "created_at": row['created_at']
                })
        driver.close()
        print(f"Successfully loaded {len(combined_df)} records into Neo4j.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Error', 500

    return 'Pipeline executed successfully!', 200
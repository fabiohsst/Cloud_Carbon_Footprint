import streamlit as st
import os
import pandas as pd
from datetime import date
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_neo4j import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph

# Load environment variables from .env file
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Multi-Cloud Carbon Footprint Analyzer",
    page_icon="☁️",
    layout="wide"
)

st.title("☁️ Multi-Cloud Carbon Footprint Analyzer")
st.sidebar.header("About")
st.sidebar.info(
    "This tool allows you to ask questions in plain English or generate a detailed report about the carbon footprint of your company's multi-cloud infrastructure."
)

# --- Neo4j and LangChain Connection ---
@st.cache_resource
def init_chain():
    try:
        uri = os.environ.get("NEO4J_URI")
        username = os.environ.get("NEO4J_USERNAME")
        password = os.environ.get("NEO4J_PASSWORD")

        graph = Neo4jGraph(url=uri, username=username, password=password)
        llm = ChatOpenAI(model_name="gpt-4o-mini-2024-07-18")
        
        chain = GraphCypherQAChain.from_llm(
            graph=graph, 
            llm=llm, 
            verbose=True,
            allow_dangerous_requests=True
        )
        st.sidebar.success("Successfully connected to the database and LLM.")
        return chain, graph

    except Exception as e:
        st.sidebar.error(f"Failed to connect: {e}", icon="🚨")
        return None, None

chain, graph = init_chain()

# --- Natural Language Q&A Interface ---
st.header("Ask a question about your cloud carbon footprint:")
question = st.text_input("e.g., What is our total cloud carbon footprint?", placeholder="Ask your question here...")

if question:
    st.write(f"**Your question:** {question}")
    if chain:
        with st.spinner("The agent is thinking..."):
            try:
                response = chain.invoke({"query": question})
                st.success("Here is the answer:", icon="✅")
                st.write(response.get("result", "No result found."))
            except Exception as e:
                st.error(f"An error occurred: {e}", icon="🚨")
    else:
        st.error("The application is not connected. Please check your credentials.")

st.divider()

# --- New Reporting Interface ---
st.header("Generate a Detailed Report")

# Date input widgets for the report
start_date = st.date_input("Start date", value=date(2025, 1, 1))
end_date = st.date_input("End date", value=date(2025, 12, 31))

def generate_report(graph_connection, start, end):
    """
    Generates a detailed report by running a specific Cypher query.
    """
    cypher_query = """
    MATCH (c:Company)-[:USES_PROVIDER]->(cp:CloudProvider)-[:HAS_PROJECT]->(p:Project)-[:GENERATED]->(cr:CarbonReport)
    WHERE date({year: cr.year, month: cr.month, day: 1}) >= date($start_date)
      AND date({year: cr.year, month: cr.month, day: 1}) <= date($end_date)
    RETURN
      cp.name AS cloud_provider,
      p.id AS project_id,
      cr.service AS service,
      cr.region AS region,
      cr.year AS year,
      cr.month AS month,
      (cr.scope1 + cr.scope2 + cr.scope3) AS total_emissions
    ORDER BY total_emissions DESC
    """
    
    # Use the graph object's query method, which returns a pandas DataFrame
    report_df = graph_connection.query(cypher_query, params={"start_date": start.isoformat(), "end_date": end.isoformat()})
    return report_df

if st.button("Generate Report"):
    if graph:
        with st.spinner("Generating your report..."):
            try:
                report_data = generate_report(graph, start_date, end_date)
                st.success("Report generated successfully!", icon="📊")
                st.dataframe(report_data)

                # Display a summary
                total_emissions = report_data['total_emissions'].sum()
                st.metric(label="Total Emissions for Period (kgCO₂e)", value=f"{total_emissions:,.2f}")

            except Exception as e:
                st.error(f"An error occurred while generating the report: {e}", icon="🚨")
    else:
        st.error("The application is not connected. Please check your credentials.")
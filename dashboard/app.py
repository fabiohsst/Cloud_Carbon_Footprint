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
        return chain, graph, llm

    except Exception as e:
        st.sidebar.error(f"Failed to connect: {e}", icon="🚨")
        return None, None, None

chain, graph, llm = init_chain()

# --- New High-Level Reporting Interface (Moved to Top) ---
st.header("Generate a High-Level Report")

start_date_report = st.date_input("Start date", value=date(2025, 1, 1), key="report_start")
end_date_report = st.date_input("End date", value=date(2025, 12, 31), key="report_end")

def generate_aggregated_report(graph_connection, start, end):
    """
    Generates an aggregated report for graphing.
    """
    cypher_query = """
    MATCH (cp:CloudProvider)-[:HAS_PROJECT]->(p:Project)-[:GENERATED]->(cr:CarbonReport)
    WHERE date({year: cr.year, month: cr.month, day: 1}) >= date($start_date)
      AND date({year: cr.year, month: cr.month, day: 1}) <= date($end_date)
    RETURN
      cp.name AS provider,
      cr.year AS year,
      cr.month AS month,
      sum(cr.scope1 + cr.scope2 + cr.scope3) AS total_emissions
    ORDER BY year, month, provider
    """
    result = graph_connection.query(cypher_query, params={"start_date": start.isoformat(), "end_date": end.isoformat()})
    report_df = pd.DataFrame(result)
    return report_df

def get_llm_insights(report_dataframe, llm_connection):
    """
    Sends the report data to an LLM to generate insights.
    """
    # Convert the DataFrame to a string format for the LLM
    data_string = report_dataframe.to_string()
    
    prompt = f"""
    You are a senior data analyst specializing in cloud carbon footprints. 
    Based on the following data, provide a high-level summary and three key actionable insights.
    The data shows monthly carbon emissions (in kgCO₂e) by cloud provider.

    Data:
    {data_string}

    Analysis:
    """
    
    response = llm_connection.invoke(prompt)
    return response.content


if st.button("Generate High-Level Report"):
    if graph and llm:
        with st.spinner("Generating your report and insights..."):
            try:
                # 1. Get aggregated data
                agg_data = generate_aggregated_report(graph, start_date_report, end_date_report)
                
                if not agg_data.empty:
                    st.subheader("Monthly Emissions by Provider")
                    
                    # Pivot data for charting
                    chart_data = agg_data.pivot(index='month', columns='provider', values='total_emissions')
                    
                    # 2. Create a graph
                    st.bar_chart(chart_data)
                    
                    # 3. Get LLM-generated insights
                    st.subheader("AI-Generated Insights")
                    insights = get_llm_insights(agg_data, llm)
                    st.markdown(insights)
                else:
                    st.warning("No data found for the selected period.")

            except Exception as e:
                st.error(f"An error occurred while generating the report: {e}", icon="🚨")
    else:
        st.error("The application is not connected. Please check your credentials.")

st.divider()

# --- Natural Language Q&A Interface (Moved to Bottom) ---
st.header("Ask a Specific Question")
question = st.text_input("e.g., What is our total cloud carbon footprint?", placeholder="Ask your question here...", key="qa_input")

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
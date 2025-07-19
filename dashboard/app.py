import streamlit as st
import os
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
    "This tool allows you to ask questions in plain English about the "
    "carbon footprint of your company's multi-cloud infrastructure."
)

# --- Neo4j and LangChain Connection ---
@st.cache_resource
def init_chain():
    try:
        # Get Neo4j credentials from environment variables
        uri = os.environ.get("NEO4J_URI")
        username = os.environ.get("NEO4J_USERNAME")
        password = os.environ.get("NEO4J_PASSWORD")

        # Initialize the Neo4j graph connection
        graph = Neo4jGraph(url=uri, username=username, password=password)
        
        # Initialize the OpenAI LLM
        # It will automatically use the OPENAI_API_KEY from your .env file
        llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18")
        
        # Create the Question-Answering chain
        chain = GraphCypherQAChain.from_llm(
            graph=graph, 
            llm=llm, 
            verbose=True,
            allow_dangerous_requests=True
        )
        st.sidebar.success("Successfully connected to the database and LLM.")
        return chain

    except Exception as e:
        st.sidebar.error(f"Failed to connect: {e}", icon="🚨")
        return None

chain = init_chain()

# --- User Interface ---
st.header("Ask a question about your cloud carbon footprint:")
question = st.text_input("e.g., What is our total cloud carbon footprint?", placeholder="Ask your question here...")

if question:
    st.write(f"**Your question:** {question}")
    
    # --- Agent Execution ---
    if chain:
        with st.spinner("The agent is thinking..."):
            try:
                response = chain.invoke({"query": question})
                st.success("Here is the answer:", icon="✅")
                st.write(response.get("result", "No result found."))
            except Exception as e:
                st.error(f"An error occurred: {e}", icon="🚨")
    else:
        st.error("The application is not connected to the database. Please check your credentials in the .env file and restart.")
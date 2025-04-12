import streamlit as st
import pandas as pd
import torch
import hashlib
from sentence_transformers import SentenceTransformer, util

# ------------------
# Set Page Config – Must be the first Streamlit command!
# ------------------
st.set_page_config(page_title="Creator Matching App", layout="wide")

# ------------------
# Caching & Model
# ------------------
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer("BAAI/bge-m3")

# ------------------
# Helper Functions
# ------------------
def load_dataset(uploaded_file):
    """
    Load a CSV or Excel file from the uploaded file.
    Raises ValueError if the file format is unsupported.
    """
    file_name = uploaded_file.name.lower()
    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif file_name.endswith((".xls", ".xlsx")):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file format. Upload a CSV or Excel file.")
    return df

def validate_dataset(df, required_cols):
    """
    Check that the loaded dataset has all required columns.
    """
    if not required_cols.issubset(set(df.columns)):
        raise ValueError(f"Dataset must include the following columns: {required_cols}")

def display_creator_card(row):
    """
    Display one creator as a styled HTML card.
    """
    card_html = f"""
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
        <h3 style="margin-bottom: 5px;">{row['name']}</h3>
        <p>
            <strong>Niche:</strong> {row['niche']} |
            <strong>Location:</strong> {row['location']} |
            <strong>Audience:</strong> {row['audience_size']}
        </p>
        <p style="color: #006600;"><strong>Similarity Score:</strong> {row['similarity_score']:.4f}</p>
        <p><em>{row['bio']}</em></p>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def embed_and_score(creators_df, campaign_brief, model):
    """
    Embed the creator bios and the campaign brief, then compute cosine similarity.
    Returns a DataFrame with similarity scores.
    """
    # Embed creator bios
    bio_texts = creators_df["bio"].tolist()
    bio_embeddings = model.encode(bio_texts, convert_to_tensor=False, normalize_embeddings=True)
    creators_df = creators_df.copy()
    creators_df["bio_embedding"] = bio_embeddings.tolist()
    
    # Embed campaign brief with the recommended prompt.
    query = "Represent this sentence for searching relevant passages: " + campaign_brief
    query_embedding = model.encode(query, convert_to_tensor=True, normalize_embeddings=True)
    
    # Compute cosine similarity
    device = query_embedding.device
    creator_embeddings_tensor = torch.tensor(bio_embeddings, device=device)
    similarities = util.cos_sim(query_embedding, creator_embeddings_tensor)[0].cpu().numpy()
    creators_df["similarity_score"] = similarities
    
    return creators_df.drop(columns=["bio_embedding"])

# -------------------------------
# Main Streamlit App – Creator Matching
# -------------------------------
st.title("🔍 Creator Matching App")
st.markdown("### Upload your creator dataset (CSV or Excel format)")

# File uploader – only proceed if a file is provided.
uploaded_file = st.file_uploader("📁 Upload your creator dataset", type=["csv", "xlsx"])
if uploaded_file is None:
    st.info("Please upload your dataset to get started.")
    st.stop()

# -------------------------------
# Step 1: Load and Validate Dataset
# -------------------------------
try:
    creators_df = load_dataset(uploaded_file)
    required_cols = {"name", "bio", "niche", "location", "audience_size"}
    validate_dataset(creators_df, required_cols)
    st.success(f"✅ Dataset loaded successfully with {len(creators_df)} creators.")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# -------------------------------
# Step 2: Campaign Brief Input within a Form
# -------------------------------
st.markdown("### Enter your campaign brief and then click 'Calculate Embeddings'")
with st.form("embedding_form"):
    campaign_brief = st.text_area("Campaign Brief", placeholder="e.g. Looking for Indian influencers who focus on eco-friendly fashion and modern lifestyle.")
    submit_button = st.form_submit_button("🔁 Calculate Embeddings")

if campaign_brief.strip() == "":
    st.info("Please enter a campaign brief to find matches.")
    st.stop()

# -------------------------------
# Step 3: Compute Embeddings (when form is submitted or cache is not valid)
# -------------------------------
# Create a unique cache key from file content and campaign brief.
file_hash = hashlib.sha256(uploaded_file.getvalue()).hexdigest()
brief = campaign_brief.strip()

if submit_button or ("scored_df" not in st.session_state or st.session_state.get("last_file_hash") != file_hash or st.session_state.get("last_brief") != brief):
    with st.spinner("Embedding campaign brief and calculating similarity..."):
        try:
            model = load_model()
            scored_df = embed_and_score(creators_df, brief, model)
            st.session_state.scored_df = scored_df
            st.session_state.last_file_hash = file_hash
            st.session_state.last_brief = brief
        except Exception as e:
            st.error(f"Error during embedding and scoring: {e}")
            st.stop()
else:
    scored_df = st.session_state.scored_df
    st.info("✅ Using cached embedding results. Click 'Calculate Embeddings' to refresh.")

# -------------------------------
# Step 4: Sidebar Filters and Top Match Count
# -------------------------------
st.sidebar.header("🔧 Filter Results")
unique_niches = sorted(scored_df["niche"].dropna().unique())
unique_locations = sorted(scored_df["location"].dropna().unique())

selected_niche = st.sidebar.selectbox("Filter by Niche", ["All"] + unique_niches)
selected_location = st.sidebar.selectbox("Filter by Location", ["All"] + unique_locations)
top_count = st.sidebar.slider("Number of Top Matches", min_value=1, max_value=50, value=10, step=1)

filtered_df = scored_df.copy()
if selected_niche != "All":
    filtered_df = filtered_df[filtered_df["niche"] == selected_niche]
if selected_location != "All":
    filtered_df = filtered_df[filtered_df["location"] == selected_location]

top_creators = filtered_df.sort_values(by="similarity_score", ascending=False).head(top_count)

# -------------------------------
# Step 5: Display Matching Creator Cards
# -------------------------------
st.markdown("### 🎯 Top Matching Creators")
if top_creators.empty:
    st.warning("No matching creators found. Adjust your filters or campaign brief.")
else:
    for _, row in top_creators.iterrows():
        display_creator_card(row)

# -------------------------------
# Step 6: Download Results
# -------------------------------
st.markdown("### 📥 Download Results")
csv_data = top_creators.to_csv(index=False)
st.download_button(label="Download CSV", data=csv_data, file_name="top_creators.csv", mime="text/csv")
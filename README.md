# 🎯 Creator Matching App – End-to-End Guide

## 📘 Overview

The **Creator Matching App** is a powerful and interactive Streamlit-based tool that connects **campaign briefs** to the most relevant **content creators** by leveraging **state-of-the-art large language models (LLMs)** and **semantic similarity** techniques.

It helps marketers, agencies, influencer platforms, and brands to:

- Automatically evaluate relevance between brief and creator bio
- Avoid manual screening of hundreds or thousands of profiles
- Download top matches instantly in CSV format

---

## 🚀 Key Features

| Feature                 | Description                                                                                                           |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 🧠 Semantic Search      | Uses `BAAI/bge-m3` LLM embeddings to understand meaning in campaign briefs and bios<br />(Does not require API key) |
| 🔁 Controlled Embedding | Embeddings computed **only** when the user clicks "Calculate Embeddings"                                       |
| ⚡ Fast Filtering       | Sidebar filters by niche, location, and match count                                                                   |
| 📥 Download Option      | Export top matching creators to CSV                                                                                   |
| 🧠 Smart Caching        | Uses `st.session_state` to prevent recomputation                                                                    |
| 💅 Modern UI            | Form-based input, styled cards, and dynamic elements                                                                  |

---

## 📂 Required Dataset Format

Upload your file (`.csv` or `.xlsx`) with these **mandatory columns**:

| Column            | Description                                               |
| ----------------- | --------------------------------------------------------- |
| `name`          | Creator’s full name or handle                            |
| `bio`           | A free-text bio, e.g., "Lifestyle & fashion creator       |
| `niche`         | Creator’s category or genre (e.g., beauty, tech, gaming) |
| `location`      | City, state, or region (e.g., Mumbai, Bangalore)          |
| `audience_size` | A number indicating follower count or audience reach      |

🟡 **Important:** Missing any of these columns will cause the app to stop with a clear error.

---

## 💡 How It Works: Step by Step

### Step 1: Upload File

You upload a `.csv` or `.xlsx` file containing creator data.

### Step 2: Write Campaign Brief

You enter a campaign brief like:

```
Looking for creators in India who specialize in tech reviews, YouTube Shorts, and have more than 50K followers.
```

### Step 3: Click "Calculate Embeddings"

- Creator bios are embedded using `BAAI/bge-m3`
- Campaign brief is embedded using the **recommended prompt**:
  > Represent this sentence for searching relevant passages: [your brief]
  >

### Step 4: Compute Similarity

Cosine similarity is calculated between the brief and each bio, resulting in a relevance score (0 to 1) per creator.

### Step 5: Filter & Sort

In the sidebar, you can:

- Filter by **niche**
- Filter by **location**
- Set how many top matches to show using a slider

### Step 6: View & Download

Top creators are displayed as styled cards with their similarity score. A download button allows exporting to CSV.

---

## 📦 Installation Instructions

### Step 1: Clone Repo

## 📌 Model Used: `BAAI/bge-m3`

- High-performing sentence embedding model from BAAI (Beijing Academy of AI)
- Trained for multilingual semantic search & retrieval
- Supports input prompts for improved alignment
- Output vector: **1024 dimensions**

**Embedding Prompt (recommended by BGE):**

```text
"Represent this sentence for searching relevant passages: " + [your text]
```

---

## ⚙️ Internal Design & Caching

| Component                      | Purpose                                           |
| ------------------------------ | ------------------------------------------------- |
| `@st.cache_resource`         | Loads the embedding model once and reuses it      |
| `st.session_state`           | Stores cached embeddings, dataset hash, and brief |
| `torch.tensor` + `cos_sim` | Efficient cosine similarity computation           |
| `st.form`                    | Groups the brief + button UI                      |
| `st.download_button`         | One-click export of results                       |

📁 **Hashing** is used to detect if the uploaded file or brief has changed. If not, results are reused.

---

## 🧪 Example Dataset Entry

```csv
name,bio,niche,location,audience_size
Neha Sharma,"Fashion & lifestyle influencer | Vegan recipes | 180k Instagram",Fashion,Mumbai,180000
Aman Raj,"Tech enthusiast | Gadget reviews | Shorts expert",Tech,Delhi,95000
```

## 🧠 Example Campaign Brief

```
	Looking for Indian beauty influencers who can create engaging reels around skincare products.
```

## 📌 Output (Top Match)

```json
{
  "name": "Ananya R.",
  "niche": "Beauty",
  "location": "Bangalore",
  "audience_size": 120000,
  "similarity_score": 0.932,
  "bio": "Beauty & skincare reels | Natural products | Based in Bangalore | 120k strong "
}
```

---

## 📎 Files in This Project

| File                          | Description                   |
| ----------------------------- | ----------------------------- |
| `creator_identification.py` | Main Streamlit app            |
| `README.md`                 | This documentation            |
| `requirements.txt`          | Required packages             |
| `creator_df.csv`            | (Example dataset if provided) |

---

## 🧠 Why LLM-Based Matching Works

- LLMs can detect **semantic overlap** beyond keyword matching
- They handle synonyms, structure, and even *intent*
- Great for sparse bios or brief phrasing differences

**Examples:**
`eco-conscious` ≈ `sustainable`
`beauty influencer` ≈ `skincare creator`
`short videos` ≈ `reels`, `shorts`, `YouTube Shorts`

---
Streamlit: https://creatorandbriefsmatching-mgrlgc6hgahs9uvlodiwwi.streamlit.app/

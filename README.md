# Creator Matching App 🎯

This is a powerful Streamlit-based application designed to help brands and marketers match their **campaign briefs** with the most relevant **influencers or content creators** using **Large Language Model (LLM)**-based semantic similarity techniques.

It uses pretrained embeddings from `BAAI/bge-m3` (a top-tier model from Hugging Face) and computes **cosine similarity** between campaign briefs and creator bios to identify the best matches.

---

## 📌 Use Case

Suppose you're a brand looking for creators to promote a new eco-friendly fashion line in India. Instead of manually going through thousands of bios, you simply:

1. Upload your dataset of creators
2. Enter a brief like: *"Looking for Indian influencers who focus on eco-friendly fashion and modern lifestyle."*
3. Click **Calculate Embeddings**
4. The app gives you a ranked list of top-matching creators with similarity scores and filters to narrow your selection.

---

## 📊 Input Dataset Format

Upload a `.csv` or `.xlsx` file with the following **required columns**:

| Column         | Description                                      |
|----------------|--------------------------------------------------|
| `name`         | Creator’s name                                   |
| `bio`          | Creator’s bio/description                        |
| `niche`        | Primary content category (e.g., fashion, tech)   |
| `location`     | Where the creator is based (e.g., Delhi, Mumbai) |
| `audience_size`| Number of followers or reach estimate            |

---

## 🧠 How It Works

### 1. **Embeddings Generation**
- Creator bios are passed through the `BAAI/bge-m3` embedding model to generate 1024-dimensional vectors.
- The campaign brief is also embedded with a special prefix recommended by BGE:  
  `"Represent this sentence for searching relevant passages: "`

### 2. **Similarity Calculation**
- Cosine similarity is calculated between the campaign brief embedding and each creator bio embedding.
- These scores are added to the dataframe under the column `similarity_score`.

### 3. **Filtering & Sorting**
- Use interactive filters in the sidebar to select niche, location, and number of top creators to display.
- Top results are shown in styled cards with the bio and similarity score.

### 4. **Download**
- The final list of top matches can be downloaded as a `.csv` file.

---

## 🚀 Features

-> Upload Excel or CSV creator datasets  
-> Campaign brief input with interactive submission  
-> Caching of results (no redundant computation)  
-> Styled creator cards with clear similarity scores  
-> Filter by niche and location  
-> Slider to choose number of top matches  
-> Download top results as CSV  
-> Optimized for performance using `@st.cache_resource` and `st.session_state`  
-> Streamlit-compatible with `st.set_page_config` called correctly at top

---

## 🧰 Technologies Used

- [Streamlit](https://streamlit.io) – interactive UI
- [sentence-transformers](https://www.sbert.net/) – semantic embeddings
- [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) – state-of-the-art multilingual embedding model
- [PyTorch](https://pytorch.org/) – tensor and similarity operations
- [pandas](https://pandas.pydata.org/) – data wrangling

---

## 📦 Installation

```bash
pip install streamlit pandas torch sentence-transformers openpyxl
```

Or from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run creator_identification.py
```

---

## ✅ Model: BAAI/bge-m3

- Multilingual embedding model optimized for retrieval use cases.
- Usage follows best practice by adding:  
  `"Represent this sentence for searching relevant passages: "` to the input prompt.
- Supports efficient, high-dimensional similarity matching.

---

## 🧠 Behind the Scenes

- All embeddings are normalized before similarity calculation
- Cosine similarity scores are used to rank results
- Embedding is only recalculated when:
  - The campaign brief changes
  - A new dataset is uploaded
  - OR the "🔁 Calculate Embeddings" button is clicked

---

## 🖼️ UI Highlights

- Custom button inside form to tightly pair it with brief input
- Sidebar filters auto-update the visible creator cards
- Downloadable CSV makes exporting simple
- All results are cached until changed

---

## 🛠️ Example Entry

**Brief:** `Looking for Indian beauty influencers in tier-1 cities who specialize in reels.`  
**Top Result:**

```json
{
  "name": "Aditi Sharma",
  "niche": "Beauty",
  "location": "Delhi",
  "audience_size": 240000,
  "similarity_score": 0.8941,
  "bio": "Beauty and lifestyle creator | Everyday glam | Insta reels | PR-friendly | Mumbai | 240k strong fam 💄✨"
}
```

---

## ❤️ Credits

Model powered by Hugging Face, app styled with Streamlit.


## 📧 Contact

For questions or suggestions, reach out at: **parasharranjay@gmail.com**
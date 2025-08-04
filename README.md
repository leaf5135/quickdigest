# QuickDigest

QuickDigest is a lightweight, AI-powered news summarizer. It fetches real-time headlines from NewsAPI and uses the Cerebras SDK to generate concise summaries based on the topic you select.

---

## Tech Stack

* **Backend**: FastAPI, NewsAPI, Cerebras SDK
* **Frontend**: Vue 3, Vite

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone [repo]
cd quickdigest
```

---

### 2. Backend Setup

```bash
cd quickdigest-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the `quickdigest-backend` directory and add the following environment variables:

```env
NEWSAPI_KEY=your_newsapi_key
CEREBRAS_API_KEY=your_cerebras_api_key
```

Start the backend server:

```bash
uvicorn main:app --reload
```

---

### 3. Frontend Setup

```bash
cd quickdigest-frontend
npm install
npm run dev
```

---

## Usage

Select a topic to view summarized news headlines.
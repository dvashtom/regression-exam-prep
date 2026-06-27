"""
AI Assistant Service - Lightweight RAG for Linear Regression course.
Uses FAISS directly + OpenAI-compatible API via local proxy.
No langchain, no torch, no heavy dependencies.
"""

import os
import pickle
import numpy as np
import faiss
from pathlib import Path
from typing import List, Dict, Optional

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

# Configuration
AI_PROXY_URL = os.getenv("AI_PROXY_URL", "http://localhost:6655/v1")
AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "claude-sonnet-4-20250514")
AI_API_KEY = os.getenv("AI_API_KEY", "sk-placeholder")
VECTOR_STORE_PATH = os.getenv(
    "VECTOR_STORE_PATH",
    str(Path(__file__).parent / "data" / "vector_store")
)

# System prompt
SYSTEM_PROMPT = """אתה עוזר אישי חכם ומומחה לרגרסיה לינארית עבור הסטודנטים בקורס של יקיר.
תפקידך לסייע לסטודנט בפתרון שאלות, הסבר מושגים והבנת הקשרים הסטטיסטיים.

הנחיות קשיחות:

מקורות ידע: עליך להסתמך אך ורק על המידע המופיע בקבצים המצורפים (חוברת הקורס, דף הנוסחאות ומבחני העבר). אם שאלה אינה קשורה לחומר הנלמד בקורס, ציין זאת בנימוס והפנה את הסטודנט לנושאים הרלוונטיים.

סגנון מענה:
- היה תמציתי ומדויק.
- השתמש בטרמינולוגיה המקובלת בקורס (כפי שמופיעה בדף הנוסחאות).
- כאשר אתה מסביר מושג, נסה תמיד להפנות לנוסחה הרלוונטית מ'דף נוסחאות למבחן 2025'.
- ענה בעברית.

הגבלת תחום: אם המשתמש שואל שאלות בנושאים שאינם רלוונטיים לקורס (כגון פוליטיקה, פיתוח אפליקציות או נושאים אקדמיים אחרים), השב: 'סליחה, אני מומחה אך ורק לרגרסיה לינארית עבור הקורס הנוכחי. אשמח לעזור לך בנושאי הקורס בלבד.'

שימוש בנוסחאות: במידת האפשר, הצג נוסחאות באמצעות סימון LaTeX.

הקונטקסט הרלוונטי מחומרי הקורס:
{context}
"""


class AIAssistant:
    """Lightweight AI Assistant with RAG capabilities."""

    def __init__(self):
        self._index = None
        self._metadata = None
        self._client = None

    @property
    def client(self):
        """Lazy-load the OpenAI client."""
        if self._client is None:
            self._client = OpenAI(
                base_url=AI_PROXY_URL,
                api_key=AI_API_KEY
            )
        return self._client

    def _load_index(self):
        """Load FAISS index and metadata from disk."""
        index_path = os.path.join(VECTOR_STORE_PATH, "index.faiss")
        meta_path = os.path.join(VECTOR_STORE_PATH, "metadata.pkl")

        if not os.path.exists(index_path):
            return False

        self._index = faiss.read_index(index_path)
        with open(meta_path, "rb") as f:
            self._metadata = pickle.load(f)
        return True

    def _embed_query(self, query: str) -> np.ndarray:
        """Create embedding for a query using the same hash method as indexing."""
        dim = 384
        vec = np.zeros(dim, dtype=np.float32)
        words = query.split()
        for word in words:
            h = hash(word.lower()) % dim
            vec[h] += 1.0
            if len(word) > 2:
                for j in range(len(word) - 2):
                    trigram = word[j:j+3]
                    h2 = hash(trigram) % dim
                    vec[h2] += 0.5
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.reshape(1, -1)

    def retrieve_context(self, query: str, k: int = 5) -> str:
        """Retrieve relevant context from the vector store."""
        if self._index is None:
            if not self._load_index():
                return "בסיס הנתונים לא נטען. הרץ: python data/build_vector_store.py"

        # Embed query
        query_vec = self._embed_query(query)
        faiss.normalize_L2(query_vec)

        # Search
        scores, indices = self._index.search(query_vec, k)

        # Format results
        context_parts = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < 0 or idx >= len(self._metadata):
                continue
            meta = self._metadata[idx]
            source = meta.get("source", "לא ידוע")
            doc_type = meta.get("type", "")
            type_label = {
                "course_book": "📖 חוברת הקורס",
                "formula_sheet": "📐 דף נוסחאות",
                "exam": "📝 מבחן"
            }.get(doc_type, "📄 מסמך")

            context_parts.append(
                f"--- מקור {i+1}: {type_label} - {source} ---\n{meta['text']}"
            )

        return "\n\n".join(context_parts) if context_parts else "לא נמצא מידע רלוונטי."

    def chat(self, user_message: str, chat_history: List[Dict] = None) -> str:
        """Send a message to the AI with RAG context."""
        # Retrieve relevant context
        context = self.retrieve_context(user_message)

        # Build system prompt with context
        system_prompt = SYSTEM_PROMPT.format(context=context)

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]

        # Add chat history (last 6 messages)
        if chat_history:
            for msg in chat_history[-6:]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        # Add current message
        messages.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model=AI_MODEL_NAME,
                messages=messages,
                max_tokens=2000,
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            if "Connection" in error_msg or "refused" in error_msg:
                return ("❌ לא ניתן להתחבר לשרת ה-AI. "
                        "וודא שה-Proxy המקומי פועל בכתובת: " + AI_PROXY_URL)
            return f"❌ שגיאה בתקשורת עם ה-AI: {error_msg}"

    def is_vector_store_ready(self) -> bool:
        """Check if vector store exists."""
        return os.path.exists(os.path.join(VECTOR_STORE_PATH, "index.faiss"))


# Singleton
_instance = None

def get_assistant() -> AIAssistant:
    """Get or create the singleton AI Assistant instance."""
    global _instance
    if _instance is None:
        _instance = AIAssistant()
    return _instance
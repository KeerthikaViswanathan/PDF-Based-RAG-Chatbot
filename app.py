
import os
import numpy as np
import streamlit as st

from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="PDF Expert Bot",
    page_icon="📄"
)

st.title("📄 PDF Expert Bot")

CHUNK_WORDS = 200
OVERLAP = 40
TOP_K = 4
MIN_SCORE = 0.25

GROQ_MODEL = "openai/gpt-oss-20b"


if not GROQ_API_KEY:
    st.error("GROQ_API_KEY is missing.")
    st.stop()


client = Groq(api_key=GROQ_API_KEY)


@st.cache_resource
def load_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")


def chunk_pdf(file):
    chunks = []

    reader = PdfReader(file)

    for page_no, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""
        words = text.split()

        if not words:
            continue

        step = CHUNK_WORDS - OVERLAP

        for i in range(0, len(words), step):

            chunk_words = words[i:i + CHUNK_WORDS]

            if chunk_words:

                chunks.append({
                    "page": page_no,
                    "text": " ".join(chunk_words)
                })

    return chunks


def retrieve(question, chunks, vectors, embedder):

    question_vector = embedder.encode(
        [question],
        normalize_embeddings=True
    )[0]

    scores = vectors @ question_vector

    top_indices = np.argsort(scores)[::-1][:TOP_K]

    return [
        (chunks[i], float(scores[i]))
        for i in top_indices
    ]


def answer(question, hits):

    context = "\n\n".join(
        f"[Page {chunk['page']}] {chunk['text']}"
        for chunk, score in hits
    )

    prompt = f"""
You are a PDF question-answering assistant.

Answer ONLY using the provided document context.

Rules:
1. Do not use outside knowledge.
2. Do not make up information.
3. Give a clear and concise answer.
4. Cite relevant pages like (p. 3).
5. If the answer is not available in the context, reply exactly:
"I couldn't find that in the document."

DOCUMENT CONTEXT:

{context}

QUESTION:

{question}
"""

    try:

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Answer questions only using "
                        "the supplied document context."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1,
            max_tokens=800
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Groq API error: {e}"


uploaded = st.file_uploader(
    "Upload a PDF",
    type="pdf"
)


if uploaded:

    if st.session_state.get("file_name") != uploaded.name:

        with st.spinner("Reading and indexing your PDF..."):

            embedder = load_embedder()

            chunks = chunk_pdf(uploaded)

            if not chunks:
                st.error(
                    "No readable text was found in this PDF."
                )
                st.stop()

            vectors = embedder.encode(
                [chunk["text"] for chunk in chunks],
                normalize_embeddings=True
            )

        st.session_state.update(
            file_name=uploaded.name,
            chunks=chunks,
            vectors=vectors,
            history=[]
        )

        st.success(
            f"Indexed {len(chunks)} chunks."
        )


    for role, text in st.session_state.get(
        "history",
        []
    ):

        st.chat_message(role).write(text)


    if question := st.chat_input(
        "Ask something about the PDF..."
    ):

        st.chat_message("user").write(question)

        hits = retrieve(
            question,
            st.session_state.chunks,
            st.session_state.vectors,
            load_embedder()
        )

        if not hits or hits[0][1] < MIN_SCORE:

            reply = (
                "I couldn't find that in the document."
            )

        else:

            with st.spinner("Generating answer..."):

                reply = answer(
                    question,
                    hits
                )

        st.chat_message("assistant").write(reply)

        with st.expander("📚 Sources used"):

            for chunk, score in hits:

                st.caption(
                    f"Page {chunk['page']} "
                    f"(similarity score: {score:.2f})"
                )

                st.write(
                    chunk["text"][:300] + "..."
                )

        st.session_state.history += [
            ("user", question),
            ("assistant", reply)
        ]

else:

    st.info(
        "📄 Upload a PDF to start asking questions."
    )


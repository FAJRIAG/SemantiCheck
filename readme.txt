📌 Deskripsi Singkat

SemantiCheck adalah sistem pendeteksi plagiarisme berbasis kemiripan semantik (semantic similarity) menggunakan teknologi Natural Language Processing (NLP) dan AI sentence embeddings.
Sistem ini mampu mendeteksi parafrase, restrukturisasi kalimat, dan pengubahan kata, bukan hanya copy–paste.

⚠️ Catatan: Sistem ini memberikan indikasi probabilistik, bukan vonis plagiarisme.

🎯 Tujuan Proyek

Mendeteksi plagiarisme berbasis makna teks

Mengatasi keterbatasan metode keyword matching

Menyediakan sistem yang:

Akademis

Transparan

Dapat dijelaskan (explainable)

🧠 Metodologi Utama

Sentence Transformer (Multilingual)

Embedding-based similarity

Cosine Similarity

Paragraph-level comparison

🏗️ Arsitektur Sistem
4
Komponen:

Input Text / Dokumen

Preprocessing NLP

Embedding Generator (AI Model)

Similarity Engine

Risk Classifier

Result & Explanation Layer


🧪 Kategori Hasil
Similarity Score	Risk Level
< 40%	Low
40–70%	Medium
> 70%	High

🧰 Teknologi

Python 3.9+

sentence-transformers

scikit-learn

FastAPI (opsional, API)

FAISS (opsional, large-scale)

📂 Struktur Proyek
SemantiCheck/
│
├── app/
│   ├── main.py
│   ├── embedding.py
│   ├── similarity.py
│   ├── analyzer.py
│   └── prompts/
│       └── plagiarism_prompt.txt
│
├── data/
│   └── reference_texts/
│
├── requirements.txt
└── README.md

⚖️ Etika & Disclaimer

Sistem tidak memberikan keputusan final

Hasil harus dikombinasikan dengan review manusia

Digunakan untuk pendidikan & penelitian
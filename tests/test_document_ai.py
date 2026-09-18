def test_text_extraction(tmp_path):
 from backend.services.document_ai import DocumentAI
 p=tmp_path/"a.txt";p.write_text("বাংলা document",encoding="utf-8")
 assert "বাংলা" in DocumentAI().extract(p)["text"]
def test_rag(tmp_path):
 from backend.core.rag import RAGStore
 r=RAGStore(tmp_path/"r.db");r.add("1","hello bengali");assert r.search("bengali")[0]["doc_id"]=="1"

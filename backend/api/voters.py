"""Voter intelligence APIs."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from backend.voter_ai import VoterStore, extract_and_store

router=APIRouter(prefix="/api/voters",tags=["voter-ai"])
store=VoterStore()

class ImportRequest(BaseModel):
 document_id:str=Field(min_length=1,max_length=200)
 text:str=Field(min_length=1,max_length=2_000_000)

class SearchRequest(BaseModel):
 query:str=Field(min_length=1,max_length=1000)
 limit:int=Field(default=50,ge=1,le=200)

@router.get("/stats")
def stats(): return store.stats()

@router.post("/import-text")
def import_text(req:ImportRequest): return extract_and_store(req.document_id,req.text,store)

@router.post("/search")
def search(req:SearchRequest): return {"results":store.search(req.query,req.limit)}

@router.get("/{voter_id}")
def get_voter(voter_id:str):
 rows=store.search(voter_id,1)
 if not rows or rows[0].get("voter_id")!=voter_id: raise HTTPException(404,"Voter record not found.")
 return rows[0]

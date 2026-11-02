from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.config import settings
from app.db.database import get_db
from app.db.models import Claim, ClaimDocument, Policy

router = APIRouter(prefix="/api/v1/claims", tags=["claims"])


class ClaimCreate(BaseModel):
    policy_number: str | None = None
    incident_type: str = Field(min_length=1, max_length=60)
    incident_date: str | None = None
    incident_location: str | None = Field(default=None, max_length=180)
    description: str = Field(min_length=5, max_length=4000)


ALLOWED_DOCUMENT_TYPES = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def _matches_file_signature(content_type: str, content: bytes) -> bool:
    signatures = {
        "application/pdf": content.startswith(b"%PDF-"),
        "image/jpeg": content.startswith(b"\xff\xd8\xff"),
        "image/png": content.startswith(b"\x89PNG\r\n\x1a\n"),
        "image/webp": len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WEBP",
    }
    return signatures.get(content_type, False)


@router.get("/{reference_id}")
def get_claim(reference_id: str, db: Session = Depends(get_db)):
    claim = db.query(Claim).filter(Claim.reference_id == reference_id.upper()).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim reference was not found.")
    return {
        "reference_id": claim.reference_id,
        "incident_type": claim.incident_type,
        "incident_date": claim.incident_date,
        "incident_location": claim.incident_location,
        "description": claim.description,
        "status": claim.status,
        "status_message": claim.status_message,
        "created_at": claim.created_at,
        "documents": [
            {
                "id": document.id,
                "filename": document.filename,
                "content_type": document.content_type,
                "size_bytes": document.size_bytes,
            }
            for document in claim.documents
        ],
    }


@router.post("/{reference_id}/documents", status_code=201)
async def upload_claim_documents(
    reference_id: str,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    claim = db.query(Claim).filter(Claim.reference_id == reference_id.upper()).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim reference was not found.")
    if not files:
        raise HTTPException(status_code=400, detail="Select at least one document.")
    if len(files) > 5:
        raise HTTPException(status_code=413, detail="Upload no more than 5 documents at a time.")

    max_bytes = settings.max_document_size_mb * 1024 * 1024
    upload_dir = Path(settings.upload_dir).resolve()
    upload_dir.mkdir(parents=True, exist_ok=True)
    saved_paths: list[Path] = []
    documents: list[ClaimDocument] = []

    try:
        for upload in files:
            extension = ALLOWED_DOCUMENT_TYPES.get(upload.content_type or "")
            if not extension:
                raise HTTPException(
                    status_code=415,
                    detail="Documents must be PDF, JPEG, PNG, or WebP files.",
                )
            content = await upload.read(max_bytes + 1)
            if not content:
                raise HTTPException(status_code=400, detail="A selected document is empty.")
            if len(content) > max_bytes:
                raise HTTPException(
                    status_code=413,
                    detail=f"Each document must be at most {settings.max_document_size_mb} MB.",
                )
            if not _matches_file_signature(upload.content_type or "", content):
                raise HTTPException(
                    status_code=415,
                    detail="A document's contents do not match its file type.",
                )
            storage_name = f"{uuid4().hex}{extension}"
            destination = upload_dir / storage_name
            destination.write_bytes(content)
            saved_paths.append(destination)
            documents.append(
                ClaimDocument(
                    claim_id=claim.id,
                    filename=Path((upload.filename or "document").replace("\\", "/")).name[:255],
                    content_type=upload.content_type or "application/octet-stream",
                    storage_name=storage_name,
                    size_bytes=len(content),
                )
            )
        db.add_all(documents)
        db.commit()
    except Exception:
        db.rollback()
        for path in saved_paths:
            path.unlink(missing_ok=True)
        raise

    return {
        "documents": [
            {
                "id": document.id,
                "filename": document.filename,
                "content_type": document.content_type,
                "size_bytes": document.size_bytes,
            }
            for document in documents
        ]
    }


@router.get("/{reference_id}/documents/{document_id}")
def download_claim_document(
    reference_id: str, document_id: int, db: Session = Depends(get_db)
):
    document = (
        db.query(ClaimDocument)
        .join(Claim)
        .filter(
            Claim.reference_id == reference_id.upper(),
            ClaimDocument.id == document_id,
        )
        .first()
    )
    if not document:
        raise HTTPException(status_code=404, detail="Claim document was not found.")
    upload_dir = Path(settings.upload_dir).resolve()
    path = (upload_dir / document.storage_name).resolve()
    if path.parent != upload_dir or not path.is_file():
        raise HTTPException(status_code=404, detail="Claim document file is not available.")
    return FileResponse(
        path,
        media_type=document.content_type,
        filename=document.filename,
        content_disposition_type="attachment",
    )


@router.post("", status_code=201)
def create_claim(payload: ClaimCreate, db: Session = Depends(get_db)):
    policy = None
    if payload.policy_number:
        policy = db.query(Policy).filter(Policy.policy_number == payload.policy_number).first()
        if not policy:
            raise HTTPException(status_code=404, detail="Policy number was not found.")
    claim = Claim(
        reference_id=f"CLM-{uuid4().hex[:8].upper()}",
        user_id=policy.user_id if policy else None,
        policy_id=policy.id if policy else None,
        incident_type=payload.incident_type,
        incident_date=payload.incident_date,
        incident_location=payload.incident_location,
        description=payload.description,
        status="SUBMITTED",
        status_message="Claim received. Our team will verify the details and documents.",
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return {
        "reference_id": claim.reference_id,
        "status": claim.status,
        "status_message": claim.status_message,
    }

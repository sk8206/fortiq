"""Migration API routes (Phase 3 implementation)."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status, BackgroundTasks

from app.core.dependencies import CurrentUser, DbSession
from app.repositories.job_repository import JobRepository
from app.repositories.migration_repository import AuditRepository
from app.schemas.common import PaginationMeta, ResponseEnvelope, ok
from app.schemas.job import JobStatus
from app.schemas.migration import AuditLogEntry, AuditLogFilters, MigrateRequest, PQCDemoResult

router = APIRouter()


@router.post("", response_model=ResponseEnvelope[dict])
async def trigger_migration(
    request: MigrateRequest,
    db: DbSession,
    user: CurrentUser,
    background_tasks: BackgroundTasks,
):
    """Trigger PQC migration job in background."""
    from sqlalchemy import select
    from app.models.endpoint import Endpoint
    from app.tasks.migrate_task import run_migration_task

    # Resolve endpoint IDs
    if request.endpoint_ids:
        endpoint_ids = [str(eid) for eid in request.endpoint_ids]
    elif request.tier:
        # Get all endpoints of specified tier
        result = await db.execute(
            select(Endpoint.id).where(Endpoint.risk_tier == request.tier)
        )
        endpoint_ids = [str(row[0]) for row in result.all()]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide either endpoint_ids or tier",
        )

    # Create job
    repo = JobRepository(db)
    total = len(endpoint_ids)
    job = await repo.create(job_type="migrate", total=total)
    await db.commit()

    # Trigger in-process BackgroundTask (No Celery/Redis needed)
    background_tasks.add_task(run_migration_task, None, str(job.id), endpoint_ids)

    return ok({"job_id": str(job.id), "status": "pending", "total": total})



@router.get("/jobs/{job_id}", response_model=ResponseEnvelope[JobStatus])
async def get_migration_job_status(
    job_id: UUID,
    db: DbSession,
    user: CurrentUser,
):
    """Get migration job status."""
    repo = JobRepository(db)
    job = await repo.get_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )
    return ok(
        JobStatus(
            id=job.id,
            status=job.status,
            job_type=job.job_type,
            total=job.total,
            processed=job.processed,
            progress_pct=job.progress_pct,
            current_endpoint=None,
            started_at=job.started_at,
            completed_at=job.completed_at,
            error=job.error,
        )
    )


@router.get("/pqc-demo", response_model=ResponseEnvelope[dict])
async def get_pqc_demo(
    db: DbSession,
    user: CurrentUser,
):
    """Get PQC demo results (ML-KEM-768 + ML-DSA-65)."""
    from app.pqc.operations import demo_ml_kem_768, demo_ml_dsa_65

    kem_result = demo_ml_kem_768()
    sig_result = demo_ml_dsa_65()

    return ok({
        "ml_kem_768": kem_result,
        "ml_dsa_65": sig_result,
    })


@router.get("/audit-log", response_model=ResponseEnvelope[list[AuditLogEntry]])
async def get_audit_log(
    db: DbSession,
    user: CurrentUser,
    endpoint_id: UUID | None = Query(None, description="Filter by endpoint ID"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
):
    """Get paginated audit log."""
    filters = AuditLogFilters(endpoint_id=endpoint_id, page=page, per_page=per_page)
    repo = AuditRepository(db)
    entries, total = await repo.get_all(filters)

    total_pages = (total + per_page - 1) // per_page
    meta = PaginationMeta(
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
    )

    items = [AuditLogEntry.model_validate(e) for e in entries]
    return ok(items, meta)

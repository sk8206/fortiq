"""Classification API routes (Phase 2 implementation)."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status, BackgroundTasks

from app.core.dependencies import CurrentUser, DbSession
from app.repositories.job_repository import JobRepository
from app.schemas.common import ResponseEnvelope, ok
from app.schemas.job import JobStatus

router = APIRouter()


@router.post("", response_model=ResponseEnvelope[dict])
async def trigger_classification(
    db: DbSession,
    user: CurrentUser,
    background_tasks: BackgroundTasks,
):
    """Trigger VQC classification job in background."""
    from app.tasks.classify_task import classify_endpoints_task

    repo = JobRepository(db)
    job = await repo.create(job_type="classify", total=100)
    await db.commit()

    # Trigger in-process BackgroundTask (No Celery/Redis needed)
    background_tasks.add_task(classify_endpoints_task, None, str(job.id))

    return ok({"job_id": str(job.id), "status": "pending"})



@router.get("/jobs/{job_id}", response_model=ResponseEnvelope[JobStatus])
async def get_job_status(
    job_id: UUID,
    db: DbSession,
    user: CurrentUser,
):
    """Get classification job status."""
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


@router.get("/model-comparison", response_model=ResponseEnvelope[dict])
async def get_model_comparison(
    db: DbSession,
    user: CurrentUser,
):
    """Get VQC vs SVM model comparison metrics."""
    from sqlalchemy import select, func
    from app.models.model_evaluation import ModelEvaluation

    # Get latest VQC evaluation
    vqc_result = await db.execute(
        select(ModelEvaluation)
        .where(ModelEvaluation.model_type == 'vqc')
        .order_by(ModelEvaluation.trained_at.desc())
        .limit(1)
    )
    vqc_eval = vqc_result.scalar_one_or_none()

    # Get latest SVM evaluation
    svm_result = await db.execute(
        select(ModelEvaluation)
        .where(ModelEvaluation.model_type == 'svm')
        .order_by(ModelEvaluation.trained_at.desc())
        .limit(1)
    )
    svm_eval = svm_result.scalar_one_or_none()

    # Build response
    metrics = {
        "vqc": {
            "accuracy": vqc_eval.accuracy if vqc_eval else 0.0,
            "precision": vqc_eval.precision_score if vqc_eval else 0.0,
            "recall": vqc_eval.recall if vqc_eval else 0.0,
            "f1": vqc_eval.f1_score if vqc_eval else 0.0,
        },
        "svm": {
            "accuracy": svm_eval.accuracy if svm_eval else 0.0,
            "precision": svm_eval.precision_score if svm_eval else 0.0,
            "recall": svm_eval.recall if svm_eval else 0.0,
            "f1": svm_eval.f1_score if svm_eval else 0.0,
        },
    }

    if not vqc_eval and not svm_eval:
        metrics["message"] = "Model comparison not available. Run training first."

    return ok(metrics)

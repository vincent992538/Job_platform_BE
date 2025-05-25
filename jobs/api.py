
from typing import List
from datetime import date

from django.db.models import QuerySet, Q
from django.shortcuts import get_object_or_404
from ninja import Query, Router
from ninja.errors import HttpError
from ninja.pagination import paginate
from ninja_jwt.authentication import JWTAuth

from job_platform.pagination import CustomPagination
from .schemas import JobIn, JobOut, JobUpdate, JobFilterSchema, JobStatus
from .models import JobPosting
import ast


router = Router()


@router.get(
    "/",
    response=List[JobOut],
    summary="Get job list",
    auth=JWTAuth()
)
@paginate(CustomPagination)
def get_jobs(request, filters: JobFilterSchema = Query()) -> QuerySet[JobPosting]:
    jobs = JobPosting.objects.all()

    if filters.status:
        today = date.today()
        match filters.status:
            case JobStatus.active:
                jobs = jobs.filter(
                    Q(posting_date__lte=today),
                    Q(expiration_date__gte=today)
                )
            case JobStatus.expired:
                jobs = jobs.filter(Q(expiration_date__lt=today))
            case JobStatus.scheduled:
                jobs = jobs.filter(Q(posting_date__gt=today))
        filters.status = None
    order = 'id'
    if filters.ordering:
        order = filters.ordering
        filters.ordering = None
    jobs = filters.filter(jobs)

    jobs = jobs.order_by(order)
    for j in jobs:  # due to sqlite don't supprot json type need to reformat data
        skills = ast.literal_eval(j.required_skills)
        j.required_skills = skills
    return jobs


@router.get(
    "/{int:job_id}",
    response=JobOut,
    summary="Get a job",
    auth=JWTAuth()
)
def get_job(request, job_id: int) -> JobPosting:
    job = get_object_or_404(JobPosting, id=job_id)
    # due to sqlite don't supprot json type need to reformat data
    job.required_skills = ast.literal_eval(job.required_skills)
    return job


@router.post(
    "/",
    response={201: dict},
    summary="Create job",
    auth=JWTAuth()
)
def create_jobs(request, job_in: JobIn) -> tuple[int, dict]:
    job = JobPosting.objects.create(
        **job_in.dict()
    )
    return 201, {'id': job.id, 'title': job.title}


@router.put(
    "/{int:job_id}",
    response=JobOut,
    summary="Update job",
    auth=JWTAuth()
)
def update_job(request, job_id: int, job_up: JobUpdate):
    job = get_object_or_404(JobPosting, id=job_id)

    u_posting_date = job_up.posting_date or job.posting_date
    u_expiration_date = job_up.expiration_date or job.expiration_date

    if u_posting_date >= u_expiration_date:
        raise HttpError(400, "Expriration date must be after posting date.")

    for field, value in job_up.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    job.save()
    if isinstance(job.required_skills, str):  # if not changing skills the format will be str
        job.required_skills = [
            skill.strip() for skill in job.required_skills.split(',')
        ]
    return job


@router.delete(
    "/{int:job_id}",
    summary="Delete job",
    response={204: None},
    auth=JWTAuth()
)
def delete_job(request, job_id: int):
    job = get_object_or_404(JobPosting, id=job_id)
    job.delete()
    return 204

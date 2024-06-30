from fastapi import APIRouter
from app.utils.fetch_summary import fetch_summary

router = APIRouter()


# url을 받아 summary를 실행하는 endpoint
@router.post("/summary")
async def get_summary(url: str):
    summary_data = await fetch_summary(url)
    return {
        "summary": summary_data[0],
        "skill_category": summary_data[1],
        "job_category": summary_data[2],
    }

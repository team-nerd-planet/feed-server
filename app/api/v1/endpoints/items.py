from fastapi import APIRouter
from app.utils.refresh_rss_feeds import refresh_rss_feeds
from app.utils.fetch_rss_feeds import fetch_rss_feeds

router = APIRouter()


@router.get("/")
def read_items():
    return [{"item_id": "foo"}, {"item_id": "bar"}]


@router.post("/refresh")
async def refresh():
    # 모든 items를 삭제하고 다시 생성
    await refresh_rss_feeds()
    return True


@router.post("/one_day_fetch")
async def one_day_fetch():
    # 모든 items를 삭제하고 다시 생성
    result = await fetch_rss_feeds()
    return {"success": result}

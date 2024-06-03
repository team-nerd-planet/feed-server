from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_items():
    return [{"item_id": "foo"}, {"item_id": "bar"}]

@router.post("/refresh")
async def refresh():
    # 모든 items를 삭제하고 다시 생성
    await refresh_rss_feeds()
    return True

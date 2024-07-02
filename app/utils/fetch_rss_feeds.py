import feedparser
import datetime
import re
import requests
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import asyncio
from app.utils.fetch_summary import fetch_summary
from app.db.session import SessionLocal
from app.db.models import Item, ItemJobTag, ItemSkillTag

job_tags = {
    "FE": 1,
    "BE": 2,
    "DEVOPS": 3,
    "SECURITY": 4,
    "DATA": 5,
    "AI": 6,
    "LLM": 7,
    "BLOCKCHAIN": 8,
    "ETC": 9,
}

skill_tags = {
    "TYPESCRIPT": 1,
    "PYTHON": 2,
    "KOTLIN": 3,
    "GO": 4,
    "RUBY": 5,
    "C++": 6,
    "C": 7,
    "JAVA": 8,
    "C#": 9,
    "PHP": 10,
    "ETC": 11,
}

feed_urls = [
    # 카카오
    "https://tech.kakao.com/blog/feed",
    # 왓챠
    "https://medium.com/feed/watcha",
    # 컬리
    "https://helloworld.kurly.com/feed",
    # 우아한형제들
    "https://techblog.woowahan.com/feed",
    # 뱅크샐러드
    "https://blog.banksalad.com/rss.xml",
    # NHN
    "https://meetup.nhncloud.com/rss",
    # 하이퍼커넥트
    "https://hyperconnect.github.io/feed",
    # 요기요
    "https://techblog.yogiyo.co.kr/feed",
    # 이스트소프트
    "https://blog.est.ai/feed",
    # 플랫팜
    "https://medium.com/feed/platfarm",
    # 스포카
    "https://spoqa.github.io/rss",
    # 네이버플레이스
    "https://medium.com/feed/naver-place-dev",
    # 라인
    "https://engineering.linecorp.com/ko/feed/index.html",
    # 리디
    "https://www.ridicorp.com/feed",
    # 네이버
    "https://d2.naver.com/d2.atom",
    # 데보션
    "https://devocean.sk.com/blog/rss.do",
    # 구글코리아
    "https://feeds.feedburner.com/GoogleDevelopersKorea",
    # AWS코리아
    "https://aws.amazon.com/ko/blogs/tech/feed",
    # 데이블
    "https://teamdable.github.io/techblog/feed",
    # 토스
    "https://toss.tech/rss.xml",
    # 스마일게이트
    "https://smilegate.ai/recent/feed",
    # 롯데온
    "https://techblog.lotteon.com/feed",
    # 카카오엔터프라이즈
    "https://tech.kakaoenterprise.com/feed",
    # 메가존클라우드
    "https://www.megazone.com/blog/feed",
    # SKC&C
    "https://engineering-skcc.github.io/feed.xml",
    # 여기어때
    "https://techblog.gccompany.co.kr/feed",
    # 원티드
    "https://medium.com/feed/wantedjobs",
    # 비브로스
    "https://boostbrothers.github.io/rss",
    # 포스타입
    "https://team.postype.com/rss",
    # 지마켓
    "https://dev.gmarket.com/feed",
    # SK플래닛
    "https://techtopic.skplanet.com/rss",
    # AB180
    "https://raw.githubusercontent.com/ab180/engineering-blog-rss-scheduler/main/rss.xml",
    # 데브시스터즈
    "https://tech.devsisters.com/rss.xml",
    # 넷마블
    "https://netmarble.engineering/feed",
    # 마키나락스
    "https://www.makinarocks.ai/blog/feed",
    # 드라마앤컴패니
    "https://blog.dramancompany.com/feed",
    # 티몬
    "https://rss.blog.naver.com/tmondev.xml",
    # 루닛
    "https://medium.com/feed/lunit",
    # 인프런
    "https://tech.inflab.com/rss.xml",
    # 게임빌컴투스플랫폼
    "https://on.com2us.com/tag/기술블로그/feed",
    # 카카오페이
    "https://tech.kakaopay.com/rss",
    # 덴티움
    "https://www.dentium.tech/rss.xml",
    # 사람인
    "https://saramin.github.io/feed",
    # 올리브영
    "https://oliveyoung.tech/rss.xml",
    # 티빙
    "https://medium.com/feed/tving-team",
    # 11번가
    "https://11st-tech.github.io/rss",
    # 다나와
    "https://danawalab.github.io/feed",
    # 농심
    "https://tech.cloud.nongshim.co.kr/feed",
    # 트렌비
    "https://tech.trenbe.com/feed",
    # 교보DTS
    "https://blog.kyobodts.co.kr/feed",
    # 중고나라
    "https://teamblog.joonggonara.co.kr/feed",
    # 씨에스리
    "https://blog.cslee.co.kr/feed",
    # 글루시스
    "https://tech.gluesys.com/feed",
    # DND
    "https://blog.dnd.ac/feed",
    # LG유플러스
    "https://techblog.uplus.co.kr/feed",
]


def get_thumbnail_from_meta(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    meta_tag = soup.find("meta", property="og:image")
    if meta_tag:
        return meta_tag["content"]
    return ""


async def fetch_summary_threaded(url):
    return await fetch_summary(url)


def parse_date(parsed_date):
    return datetime.datetime(*parsed_date[:6])


async def process_entry(
    entry,
    session,
):
    try:
        summary, skill_category, job_category = await fetch_summary_threaded(entry.link)
    except Exception as exc:
        print(f"{entry.link} generated an exception: {exc}")
        summary = entry.description if entry.description else ""

    if not summary:
        summary = entry.description if entry.description else ""

    thumbnail_url = entry.get("media_thumbnail", [{"url": None}])[0]["url"]
    if not thumbnail_url:
        thumbnail_url = get_thumbnail_from_meta(entry.link)
    entry["thumbnail"] = thumbnail_url

    if "description" not in entry or entry.description is None:
        entry["description"] = ""
    else:
        entry["description"] = re.sub(r'"', "", entry["description"])[:100]

    published_date = parse_date(entry.published_parsed)

    guid = entry.get("guid", "")
    existing_item = await session.execute(select(Item).filter_by(guid=guid))
    if existing_item.scalar_one_or_none():
        return

    new_item = Item(
        title=entry.get("title", ""),
        description=entry.get("description", ""),
        link=entry.get("link", ""),
        thumbnail=thumbnail_url,
        published=published_date,
        guid=guid,
        feed_id=entry["feed_id"],
        summary=summary,
        likes=0,
        views=0,
    )

    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)

    job_tag_id = job_tags.get(job_category, 1)
    skill_tag_id = skill_tags.get(skill_category, 1)

    new_item_job_tag = ItemJobTag(item_id=new_item.id, job_tag_id=job_tag_id)
    new_item_skill_tag = ItemSkillTag(item_id=new_item.id, skill_tag_id=skill_tag_id)

    session.add(new_item_job_tag)
    session.add(new_item_skill_tag)

    await session.commit()


async def fetch_rss_feeds():
    today = datetime.date.today()
    day_before = today - datetime.timedelta(days=1)
    tm_year, tm_mon, tm_mday = day_before.year, day_before.month, day_before.day
    entries = []

    for idx, url in enumerate(feed_urls):
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if "published_parsed" not in entry or entry.published_parsed is None:
                entry["published_parsed"] = datetime.datetime.now().timetuple()
            published_date = parse_date(entry.published_parsed)
            if (
                published_date.year >= tm_year
                and published_date.month >= tm_mon
                and published_date.day >= tm_mday
            ):
                entry["feed_id"] = idx + 1
                entries.append(entry)

    async with SessionLocal() as session:
        tasks = [process_entry(entry, session) for entry in entries]
        await asyncio.gather(*tasks)

    return True

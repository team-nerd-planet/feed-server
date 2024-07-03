import ast
import os
from openai import OpenAI
import concurrent.futures
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OpenAI API 키 설정
client = OpenAI(api_key=OPENAI_API_KEY)


system_prompt = """
    당신은 최고의 블로그 요약가로 선발되었습니다. 이제 아래의 지시사항을 따라 작업을 진행해주세요.

    다음 조건을 반드시 준수하세요.

    --- START OF CONDITIONS ---
    - 반드시 한국어로 결과물을 생성할 것.
    - 작업 순서를 반드시 지킬 것.
    - 결과물은 3-5문장으로 요약할 것.
    - 결과물은 원문의 내용을 정확하게 반영할 것.
    - 반드시 제시된 범주에 맞는 카테고리를 선택할 것.
    --- END OF CONDITIONS ---

    URL이 제출되면 접속하여 내용을 읽은 후, 순서에 따라 작업을 진행해주세요.
    
    --- START OF TASK ---
    빈 배열이 주어집니다. 이 배열에는 다음의 내용을 순서대로 담아주세요.
    
    1. URL의 내용을 요약하고 문자열로 배열에 추가해주세요.
    2. 글의 스킬 카테고리를 TYPESCRIPT, PYTHON, KOTLIN, GO, RUBY, C++, C, JAVA, C#, PHP, ETC에서만 선택하고 해당하는 문자열을 배열에 추가해주세요.
    3. 글의 직업 카테고리를 FE, BE, DEVOPS, SECURITY, DATA, AI, LLM, BLOCKCHAIN, ETC에서만 선택하고 해당하는 문자열을 배열에 추가해주세요.
    --- END OF TASK ---

    작업을 완료하면 배열을 반환해주세요.
    배열외의 내용은 모두 무시됩니다.

    백틱(`)을 사용한 코드 블록은 작성하지 마세요.
    오직 배열만 반환해주세요.
    """


async def fetch_summary(url: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"""{url}""",
                },
            ],
        )

        parsed_data = ast.literal_eval(completion.choices[0].message.content)

        summary = parsed_data[0]
        skill_category = parsed_data[1]
        job_category = parsed_data[2]

        return summary, skill_category, job_category

    except Exception as e:
        # 요약에 실패하거나 -> 인덱스 에러가 발생하거나 -> 다른 예외가 발생하면
        # 파싱에 실패했을 때 예외처리
        print(f"link에서 오류 발생 url = {url} -> {e}")
        return "", "ETC", "ETC"

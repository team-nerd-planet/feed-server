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
    2. 글의 스킬 카테고리를 TYPESCRIPT, PYTHON, KOTLIN, GO, RUBY, C++, C, JAVA, C#, PHP, ETC에서 선택하고 해당하는 문자열을 배열에 추가해주세요.
    3. 글의 직업 카테고리를 FE, BE, DEVOPS, SECURITY, DATA, AI, LLM, BLOCKCHAIN, ETC에서 선택하고 해당하는 문자열을 배열에 추가해주세요.
    마지막으로 배열 외에는 아무것도 추가하지 말고, 제출해주세요.
    --- END OF TASK ---
    """


async def fetch_summary(url: str) -> str:
    try:
        print(url)
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
        print(e)
        return "요약에 실패했습니다. 다시 시도해주세요.", None, None

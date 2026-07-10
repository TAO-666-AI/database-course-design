import requests

from core.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL


def call_deepseek(question: str) -> tuple[str, str]:
    if not DEEPSEEK_API_KEY:
        return "暂未在常见问题中找到答案，且未配置 DeepSeek API。请联系景区工作人员或查看常见问题。", "fallback"
    try:
        response = requests.post(
            DEEPSEEK_BASE_URL,
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": DEEPSEEK_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是南京中山陵景区导览管理系统的文本问答助手。请围绕中山陵、音乐台、流徽榭（水榭）、行健亭、光化亭等景点，以及开放时间、预约方式、交通方式、门票信息、游览路线、参观礼仪和游客服务进行简洁准确回答。若问题超出南京中山陵景区范围，请礼貌提示用户咨询景区官方信息。",
                    },
                    {"role": "user", "content": question},
                ],
                "temperature": 0.3,
            },
            timeout=12,
        )
        if response.status_code != 200:
            return "智能问答服务暂时不可用，请稍后再试或查看常见问题。", "fallback"
        data = response.json()
        return data["choices"][0]["message"]["content"].strip(), "deepseek"
    except Exception:
        return "智能问答服务调用失败，请稍后再试或联系景区工作人员。", "fallback"

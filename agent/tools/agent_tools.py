import os
from utils.logger_handler import logger
from langchain_core.tools import tool

from rag.rag_service import RagSummarizeService
import random
from utils.config_handler import agent_conf
from utils.path_tool import get_abs_path

rag = RagSummarizeService()

user_ids = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010",]
month_arr = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
             "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", ]

external_data = {}


@tool(description="从向量存储中检索服装相关的参考资料，包括产品信息、尺码指南、面料洗护、穿搭推荐、退换货政策等")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)


@tool(description="获取指定城市的天气信息，并以消息字符串的形式返回，包含穿搭建议")
def get_weather(city: str) -> str:
    return f"城市{city}天气为晴天，气温26摄氏度，空气湿度50%，南风3级，AQI21，最近3小时降雨概率极低。建议穿搭：短袖T恤/衬衫+薄款裤装，可选择AIRism凉感面料系列"


@tool(description="获取用户所在城市的名称，以纯字符串形式返回")
def get_user_location() -> str:
    return random.choice(["上海", "北京", "广州", "深圳", "杭州", "成都"])


@tool(description="获取用户的ID，以纯字符串形式返回")
def get_user_id() -> str:
    return random.choice(user_ids)


@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month() -> str:
    return random.choice(month_arr)


def generate_external_data():
    """
    从CSV文件加载用户购买记录数据，数据结构如下：
    {
        "user_id": {
            "month" : {"品类": xxx, "消费金额": xxx, "退换货次数": xxx, "会员等级": xxx}
            ...
        },
        ...
    }
    """
    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])

        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件{external_data_path}不存在")

        with open(external_data_path, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr: list[str] = line.strip().split(",")

                user_id: str = arr[0].replace('"', "")
                category: str = arr[1].replace('"', "")
                amount: str = arr[2].replace('"', "")
                return_count: str = arr[3].replace('"', "")
                member_level: str = arr[4].replace('"', "")
                time: str = arr[5].replace('"', "")

                if user_id not in external_data:
                    external_data[user_id] = {}

                external_data[user_id][time] = {
                    "品类": category,
                    "消费金额": amount,
                    "退换货次数": return_count,
                    "会员等级": member_level,
                }


@tool(description="从外部系统中获取指定用户在指定月份的购买记录，以纯字符串形式返回，如果未检索到返回空字符串")
def fetch_external_data(user_id: str, month: str) -> str:
    generate_external_data()

    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[fetch_external_data]未能检索到用户：{user_id}在{month}的购买记录数据")
        return ""

@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"

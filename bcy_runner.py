from fire import Fire
from pathfinder.bcy.bcy_api import BcyAPI
from datetime import datetime, timedelta


def main(
    start_date: str = "20230101",
    end_date: str = "20230612",
    target_dir: str = "results",
):
    """
    从BCY爬取榜单json
    :param start_date: 开始日期, 格式为`%Y%m%d`
    :param end_date: 结束日期, 格式为`%Y%m%d`
    :param target_dir: 结果保存目录
    """

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)

    start_date, end_date = str(start_date), str(end_date)

    start_datetime = datetime.strptime(start_date, "%Y%m%d")
    end_datetime = datetime.strptime(end_date, "%Y%m%d")

    parameters = []
    for single_date in daterange(start_datetime, end_datetime):
        for page in range(1, 5):  # pages 1 through 4
            params = {
                "p": str(page),
                "ttype": "illust",
                "sub_type": "week",
                "date": single_date.strftime("%Y%m%d"),
            }
            parameters.append(params)

    api = BcyAPI()
    api.fetch_data(parameters, target_dir=target_dir)


if __name__ == "__main__":
    # python3 bcy_runner.py --start_date="20220610" --end_date="20230610" --target_dir="jsons"
    Fire(main)

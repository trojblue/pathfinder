from pathfinder.bcy.bcy_api import BcyAPI
from datetime import datetime, timedelta


def main():

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)

    start_date = datetime.strptime("20230101", "%Y%m%d")
    end_date = datetime.strptime("20230612", "%Y%m%d")

    parameters = []
    for single_date in daterange(start_date, end_date):
        for page in range(1, 5):  # pages 1 through 4
            params = {"p": str(page), "ttype": "illust", "sub_type": "week", "date": single_date.strftime("%Y%m%d")}
            parameters.append(params)

    api = BcyAPI()
    api.fetch_data(parameters, target_dir="results")


if __name__ == '__main__':
    main()
import requests
import datetime
import pandas


class CentralBankPolicyRates:
    def __new__(cls, Country: str = None):
        Self = super().__new__(cls)

        Today = str(datetime.date.today())

        Headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " "AppleWebKit/537.36 (KHTML, like Gecko) " "Chrome/132.0.0.0 Safari/537.36"
            )
        }
        Parameters = {"page": "0", "page_size": "100"}

        JsonData = {
            "search_for": [{"search_term": "*", "field_id": ""}],
            "filters": [
                {"field_id": "CATEGORY", "search_term": "CBPOL"},
                {"field_id": "FREQ", "search_term": "D"},
                {"field_id": "TIMESPAN", "search_term": f"2000-01-01_{Today}"},
            ],
            "order_by": [{"field_id": "GLOBAL_REF_AREA_SORT", "order": "desc"}],
        }

        Response = requests.post("https://data.bis.org/api/v0/search", params=Parameters, headers=Headers, json=JsonData)
        JsonResponse = Response.json()

        DataFrame = pandas.DataFrame(JsonResponse["items"]).drop(
            columns=["df_id", "series_key", "category_id", "category_name", "frequency", "description", "unit_multiplier", "unit_code"]
        )
        DataFrame = DataFrame.rename(
            columns={
                "country": "Country",
                "country_code": "Country Code",
                "frequency_name": "Frequency",
                "title": "Title",
                "unit": "Unit",
                "start_date": "Start Date",
                "end_value": "End Value",
                "end_value_status": "End Value Status",
                "last_updated": "Last Updated",
            }
        )
        Data = DataFrame.to_dict(orient="records")
        FinData = {}
        for Item in Data:
            FinData[Item["Country"]] = Item

        if Country:
            return float(FinData.get(Country, {})["End Value"]) / 100
        else:
            return FinData

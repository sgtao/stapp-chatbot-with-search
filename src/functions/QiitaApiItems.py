# QiitaApiItems.py
from urllib.parse import urlencode

import requests

# Qiita APIのベースURL
BASE_URL = "https://qiita.com/api/v2"


class QiitaApiItems:
    def __init__(self, base_url=BASE_URL):
        self.endpoint = f"{base_url}/items"

    def get_articles(self, params=None, page_size=20, page_num=1):
        """
        Qiita APIから記事を取得するための共通関数。

        指定されたエンドポイントとオプションのパラメータを使用して、
        Qiita APIからデータを取得します。

        Args:
            query (str): クエリ文字列。デフォルト(None)の場合は最新記事を取得
            page_size (int, optional): １ページのアイテム数（`per_page`）
            pane_num (int, optional): ページ番号（`page`パラメータ）

        Returns:
          tuple(list or dict): APIからのレスポンスをJSON形式で返します。
        """

        # `query`の指定有無でアクセスURI を変化させる
        page_uri = f"{self.endpoint}?page={page_num}&per_page={page_size}"
        if params is None:
            # uri = page_uri
            uri = f"{page_uri}"
        else:
            query_string = urlencode(params)
            uri = f"{page_uri}&query={query_string}"

        print(f"request GET {uri}")
        response = requests.get(uri)

        return response.json()

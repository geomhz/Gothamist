from openpyxl import Workbook


class ExcelFile():
    def __init__(self) -> None:
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "Gothamist"

        headers = [
            "Title", "Description", "Picture Link", "Picture Name",
            "Count Phrase", "Money"
        ]

        self.ws.append(headers)

    def append_info(self, title, description, picture_link, picture_name, count_phrase, money, article_link):

        self.ws.append([
            title,
            description,
            picture_link,
            picture_name,
            count_phrase,
            money,
            article_link
        ])

    def save_file(self):
        self.wb.save(f"gothamist.xlsx")

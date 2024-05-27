from src.controller.extract_news import ExtractNewsInfo


def run():
    extract_news = ExtractNewsInfo()
    extract_news.handle_news()
    input('Pressione ENTER para encerrar...')

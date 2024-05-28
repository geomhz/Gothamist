from RPA.Browser.Selenium import Selenium

browser = Selenium()

# Abre o navegador
browser.open_available_browser("https://www.google.com")

browser.input_text("name:q", "exemplo de automação com rpaframework")

browser.press_keys("name:q", "ENTER")

browser.wait_until_page_contains_element("xpath://h3")

result_titles = browser.find_elements("xpath://h3")

for index, title in enumerate(result_titles, start=1):
    print(f"Resultado {index}: {title.text}")

input("Pressione ENTER para encerrar...")

browser.close_browser()

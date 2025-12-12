import json
from playwright.sync_api import sync_playwright


def ejecutar_scraper_playwright(query="laptops", headless=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--no-sandbox",
            ]
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            ),
            locale="es-ES",
            viewport={"width": 1280, "height": 800}
        )

        page = context.new_page()
        url = f"https://www.amazon.com/s?k={query}"
        print(f"Navegando a: {url}")
        page.goto(url, timeout=60000)

        # Espera resultados
        page.wait_for_selector('[data-component-type="s-search-result"]', timeout=20000)

        items = page.query_selector_all('[data-component-type="s-search-result"]')
        print(f"Encontrados: {len(items)} productos\n")

        productos = []

        for item in items:
            # Extraer TÍTULO
            titulo = item.query_selector("h2 a span")
            if not titulo:
                titulo = item.query_selector("h2 a")
            titulo = titulo.inner_text().strip() if titulo else "Sin título"

            # Extraer PRECIO
            precio = item.query_selector(".a-price span.a-offscreen")
            precio = precio.inner_text().strip() if precio else "Sin precio"

            # Extraer URL del producto
            enlace = item.query_selector("h2 a")
            enlace = enlace.get_attribute("href") if enlace else None
            if enlace:
                enlace = "https://www.amazon.com" + enlace

            # Guardar item
            productos.append({
                "titulo": titulo,
                "precio": precio,
                "url": enlace
            })

        # GUARDAR JSON ------------------------
        archivo = f"productos_{query}.json"
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(productos, f, indent=4, ensure_ascii=False)

        print(f"\n[OK] Guardados {len(productos)} productos en {archivo}\n")

        browser.close()


if __name__ == "__main__":
    ejecutar_scraper_playwright(query="laptops", headless=False)

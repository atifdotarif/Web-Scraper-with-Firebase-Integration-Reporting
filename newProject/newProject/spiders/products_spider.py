import scrapy

class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        "https://www.junaidjamshed.com/mens/kameez-shalwar.html"
    ]

    def parse(self, response):
        products = response.css("li.product-item")

        for item in products:
            try:
                product_id = item.css("a.product-item-photo::attr(data-product-id)").get()
                if product_id is not None:  # only yield if product_id exists
                    yield {
                        "product_id": product_id,
                        "name": item.css(".product-item-link::text").get(default="").strip(),
                        "price": float(
                            item.css(".price::text").get(default="0").replace("PKR", "").replace(",", "").strip()
                        ),
                        "availability": "Out of stock" if item.css(".stock.unavailable") else "In stock",
                        "url": item.css(".product-item-link::attr(href)").get(),
                        "image_url": item.css(".product-image-photo::attr(data-original)").get()
                    }
            except Exception as e:
                self.logger.warning(f"Error parsing item: {e}")

        next_page = response.css("li.item.pages-item-next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

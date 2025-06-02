# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class NewprojectPipeline:
#     def process_item(self, item, spider):
#         return item
from newProject.firebase_ops import upload_to_firebase

class FirebasePipeline:
    scraped_items = []

    def process_item(self, item, spider):
        self.scraped_items.append(dict(item))
        return item

    def close_spider(self, spider):
        spider.logger.info(f"Scraped {len(self.scraped_items)} items (not uploaded to Firebase).")
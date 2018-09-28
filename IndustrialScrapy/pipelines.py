# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo
from pymongo import ASCENDING

from IndustrialScrapy.items import ProjectDeclareItem, IndustrialItem, JobItem

LOG = logging.getLogger()


class IndustrialscrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPileline(object):
    ''' 存储处理管道'''
    collection_project_declare_name = 'project_declare'
    collection_industrial_name = 'industrial'
    collection_job_name = 'job'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = pymongo.MongoClient(self.mongo_uri)
        db = self.client[self.mongo_db]

        self.collection_project_declare = db[self.collection_project_declare_name]
        self.collection_project_declare.create_index([('name', ASCENDING)], unique=True)

        self.collection_industrial = db[self.collection_industrial_name]
        self.collection_industrial.create_index([('url', ASCENDING)], unique=True)

        self.collection_job = db[self.collection_job_name]
        self.collection_job.create_index([('url', ASCENDING)], unique=True)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    # def open_spider(self, spider):

    def close_spider(self, spider):
        self.client.close()

    # TODO: 日志处理,日志输出更炫！Geek
    def process_item(self, item, spider):
        try:
            if isinstance(item, ProjectDeclareItem):
                self.collection_project_declare.update_one({'name': item['name']}, {'$set': dict(item)}, upsert=True)
                LOG.info('A ProjectDeclare  recorded is added to the db')
            elif isinstance(item, IndustrialItem):
                self.collection_industrial.update_one({'url': item['url']}, {'$set': dict(item)}, upsert=True)
                LOG.info('A IndustrialItem recorded is added to the db')
        except Exception as e:
            LOG.warning('The db pipeline:{}'.format(e))
        return item

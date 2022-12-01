# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.orm import Session, declared_attr, declarative_base

class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=Base)

class MondayPost(Base):
    author = Column(String)
    date = Column(Date)
    text = Column(Text)


class MondayPostToDBPipeline:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        monday_post = MondayPost(
            author=item['author'],
            date=datetime.strptime(item['date'], "%d.%m.%Y"),
            text=item['text']
        )
        if datetime.strptime(item['date'], "%d.%m.%Y").weekday() != 0:
            raise DropItem("Этотъ постъ написанъ не въ понедѣльникъ")
        else:
            self.session.add(monday_post)
            self.session.commit()
            return item
    
    def close_spider(self, spider):
        self.session.close()

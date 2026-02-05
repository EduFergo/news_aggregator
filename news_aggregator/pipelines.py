# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import dateutil.parser

class NewsAggregatorPipeline:
    def process_item(self, item, spider):
        if not item.get('date'):
            return item

        raw_date = item['date']
        
        meses = {
            'ene': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'abr': 'Apr',
            'may': 'May', 'jun': 'Jun', 'jul': 'Jul', 'ago': 'Aug',
            'sep': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
        }

        try:
            raw_date = raw_date.strip().lower()

            if len(raw_date.split()) == 3:
                parts = raw_date.split()
                parts[1] = meses.get(parts[1][:3], parts[1]) 
                clean_date = " ".join(parts)
                dt = datetime.strptime(clean_date, "%d %b %Y")
            
            else:
                dt = dateutil.parser.parse(raw_date)

            item['date'] = dt.strftime("%Y-%m-%d %H:%M")

        except Exception as e:
            spider.logger.error(f"Error procesando fecha '{raw_date}' en {spider.name}: {e}")
        
        return item
from googleapiclient.discovery import build
from datetime import timedelta, datetime
from dotenv import load_dotenv
from typing import Any
import os

load_dotenv()


class BloggerAPI:

    def __init__(self) -> None:
        self.blog_resource = build('blogger', 'v3', developerKey=os.getenv('API_KEY'))
        self.blog = self.blog_resource.blogs().getByUrl(url=os.getenv('BLOG_URL')).execute()
        self.blog_id = self.blog.get('id')

        self.posts_resource = build('blogger', 'v3', developerKey=os.getenv('API_KEY'))
        self.processed_posts = set()
    
    def get_new_posts(self) -> list[Any]:
        """ Returns a list with posts published in the last 5 minutes """
        current_time = datetime.now()
        five_minutes_ago = current_time - timedelta(minutes=5)
        
        # Convert timestamp to RFC3339 format for google apis
        start_date = five_minutes_ago.isoformat("T") + "Z"
        # print(start_date)
        # start_date = '2024-04-24T16:09:53+00:00'

        new_posts = self.posts_resource.posts() \
            .list(blogId=self.blog_id, startDate=start_date) \
            .execute() \
            .get('items')
        
        return new_posts if new_posts else []
        
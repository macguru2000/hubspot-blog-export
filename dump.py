# coding: utf8

"""
Pulls blog content and comments from the HubSpot API
and writes them to local JSON and HTML
"""

import requests
import config
from pprint import pprint
import json
import os

class Client(object):

    """
    A convenience client for the HubSpot API
    """
    def __init__(self, hub_id, api_key,
            endpoint="https://api.hubapi.com"):
        self.hub_id = hub_id
        self.api_key = api_key
        self.endpoint = endpoint

    def __get_request(self, uri, additional_params=None):
        """Perform a GET and return a requests.Response object"""
        data = {
            "portalId": self.hub_id,
            "hapikey": self.api_key
        }
        if additional_params is not None:
            for p in additional_params.keys():
                data[p] = additional_params[p]
        url = self.endpoint + uri
        return requests.get(url, params=data)

    def iterate_blogs(self):
        """Get iterator of blogs. Will only get the first 20. (Anyone having more?)"""
        url = "/content/api/v2/blogs"
        r = self.__get_request(url)
        r.raise_for_status()
        for blog in r.json()["objects"]:
            yield blog

    def iterate_authors(self):
        """Get authors for blog"""
        url = "/blogs/v3/blog-authors"
        r = self.__get_request(url, additional_params={"limit": 100})
        r.raise_for_status()
        for author in r.json()["objects"]:
            yield author

    def iterate_topics(self):
        """Get topics for blog"""
        url = "/blogs/v3/topics"
        r = self.__get_request(url, additional_params={"limit": 100})
        r.raise_for_status()
        for topic in r.json()["objects"]:
            yield topic

    def iterate_posts(self):
        """Get iterator of blog posts of a blog"""
        url = "/content/api/v2/blog-posts"
        r = self.__get_request(url, additional_params={"limit": 100})
        r.raise_for_status()
        for post in r.json()["objects"]:
            yield post

    def iterate_comments(self):
        """Get comments for blog"""
        url = "/comments/v3/comments"
        r = self.__get_request(url, additional_params={"limit": 100})
        r.raise_for_status()
        for comment in r.json()["objects"]:
            yield comment


def main():
    hsclient = Client(config.HUBSPOT_ID, config.HUBSPOT_API_KEY)

    # root export path
    export_dir = "export"

    print("Dumping blog content to '%s'..." % export_dir)

    # export authors
    count = 0
    for author in hsclient.iterate_authors():
        folder = os.path.join(export_dir, "authors", str(author["id"]))
        if not os.path.exists(folder):
            os.makedirs(folder)
        json_filename = "%s/author_%s.json" % (folder, author["id"])
        with open(json_filename, "wb") as json_file:
            json_file.write(json.dumps(author, indent=2, sort_keys=True))
        count += 1
    print("Dumped %d authors." % count)

    # export topics
    count = 0
    # topics = []
    for topic in hsclient.iterate_topics():
        # topics.append(topic)
        # count += 1
        folder = os.path.join(export_dir, "topics", str(topic["id"]))
        if not os.path.exists(folder):
            os.makedirs(folder)
        json_filename = "%s/topic_%s.json" % (folder, topic["id"])
        with open(json_filename, "wb") as json_file:
            json_file.write(json.dumps(topic, indent=2, sort_keys=True))
        count += 1
    print("Dumped %d topics." % count)

    # export posts
    count = 0
    for post in hsclient.iterate_posts():
        folder = os.path.join(export_dir, "posts", str(post["id"]))
        if not os.path.exists(folder):
            os.makedirs(folder)
        json_filename = "%s/post_%s.json" % (folder, post["id"])
        with open(json_filename, "wb") as json_file:
            json_file.write(json.dumps(post, indent=2, sort_keys=True))
        html_filename = "%s/post_%s.html" % (folder, post["id"])
        with open(html_filename, "wb") as html_file:
            if "post_body" in post and post["post_body"] is not None:
                html_file.write(post["post_body"].encode("utf8"))
        count += 1
    print("Dumped %d posts." % count)

    # export comments
    count = 0
    for comment in hsclient.iterate_comments():
        folder = os.path.join(export_dir, "comments", str(comment["contentId"]))
        if not os.path.exists(folder):
            os.makedirs(folder)
        json_filename = "%s/comment_%s.json" % (folder, comment["id"])
        with open(json_filename, "wb") as json_file:
            json_file.write(json.dumps(comment, indent=2, sort_keys=True))
        count += 1
    print("Dumped %d comments." % count)



if __name__ == "__main__":
    main()

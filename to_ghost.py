# encoding: utf8

"""
Create Ghost-importable XML file
from blog posts and comments
"""

import os
from pprint import pprint
import json
from datetime import datetime
import time

basepath = "export"


if __name__ == "__main__":

    out = {
        "meta": {
            "exported_on": time.time(),
            "version": "003"
        },
        "data": {
            "posts": [],
            "tags": [],
            "posts_tags": [],
            "users": [],
            "roles_users": []
        }
    }




    # append all of the author objects
    for author_id in os.listdir(os.path.join(basepath, "authors")):
        subdir = os.path.join(basepath, "authors", author_id)
        author_file = "%s/author_%s.json" % (subdir, author_id)

        if not os.path.exists(author_file):
            continue

        author = None
        with open(author_file, "rb") as jsonfile:
            author = json.load(jsonfile)

        if len(author["bio"]) > 200:
            print("Truncated author bio for '%s'" % author["fullName"])

        out_user = {
            "id": author["id"],
            "name": author["fullName"],
            "slug": author["slug"],
            "email": author["email"],
            "bio": author["bio"][:200],
            "website": author["website"],
            "twitter": author["twitterUsername"],
        }

        out["data"]["users"].append(out_user)




    # append all of the tag objects
    for topic_id in os.listdir(os.path.join(basepath, "topics")):
        subdir = os.path.join(basepath, "topics", topic_id)
        topic_file = "%s/topic_%s.json" % (subdir, topic_id)

        if not os.path.exists(topic_file):
            continue

        topic = None
        with open(topic_file, "rb") as jsonfile:
            topic = json.load(jsonfile)

        if len(topic["description"]) > 200:
            print("Truncated topic description for '%s'" % topic["name"])

        out_tag = {
            "id": topic["id"],
            "name": topic["name"],
            "slug": topic["slug"],
            "description": topic["description"][:200],
        }

        out["data"]["tags"].append(out_tag)




    # append all of the post objects
    for post_id in os.listdir(os.path.join(basepath, "posts")):
        subdir = os.path.join(basepath, "posts", post_id)
        post_file = "%s/post_%s.json" % (subdir, post_id)

        if not os.path.exists(post_file):
            continue

        # read JSON file
        post = None
        with open(post_file, "rb") as jsonfile:
            post = json.load(jsonfile)

        if len(post["meta_description"]) > 200:
            print("Truncated post meta description for '%s'" % post["name"])

        out_post = {
            "id": post["id"],
            "title": post["name"],
            "slug": post["slug"],
            "markdown": post["post_body"],
            "html": post["post_body"],
            "image": None,
            "featured": 0,
            "page": 0,
            "status": "published",
            "language": "en_US",
            "meta_title": None,
            "meta_description": post["meta_description"][:200],
            "author_id": post["blog_author_id"],
            "created_at": post["created"],
            "created_by": post["blog_author_id"],
            "updated_at": post["publish_date"],
            "updated_by": post["blog_author_id"],
            "published_at": post["publish_date"],
            "published_by": post["blog_author_id"],
        }

        out["data"]["posts"].append(out_post)

        # build all the post's tag objects
        for topic_id in post["topic_ids"]:
            out_post_tag = {
                "post_id": post["id"],
                "tag_id": topic_id,
            }
            out["data"]["posts_tags"].append(out_post_tag)


    f = open("ghost.json", "wb")
    f.write(json.dumps(out, indent=2, sort_keys=True))
    f.close()

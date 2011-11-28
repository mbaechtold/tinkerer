'''
    tags
    ~~~~

    Extension handling post tagging.

    :copyright: Copyright 2011 by Vlad Riscutia.
    :license: FreeBSD, see LICENSE file
'''
from sphinx.util.compat import Directive
import tinkerer.utils


# initialize tags
def initialize(app):
    app.builder.env.blog_tags = dict()


# tags directive
class TagsDirective(Directive):
    required_arguments = 0
    optional_arguments = 100
    has_content = False

    def run(self):
        # store tags to build tag pages
        env = self.state.document.settings.env

        for tag in " ".join(self.arguments).split(","):
            tag = tag.strip()
            if tag == "none":
                continue

            if tag not in env.blog_tags:
                env.blog_tags[tag] = []
            env.blog_tags[tag].append(env.docname)
            env.blog_metadata[env.docname].tags.append(tag)

        return []


# generate tag pages
def make_tag_pages(app):
    env = app.builder.env

    # create a page for each tag
    for tag in env.blog_tags:
        pagename = "tags/" + tinkerer.utils.filename_from_title(tag)
        context = {
            "parents": [],
            "title": "Posts tagged with %s" % tag,
            "body": "<h1>Posts tagged with <em>%s</em></h1>" % tag
        }
        context["body"] += "<ul>"

        for post in env.blog_tags[tag]:
            title = env.titles[post].astext()
            context["body"] += "<li><a href=\"../%s.html\">%s</a></li>" % (post, title)

        context["body"] += "</ul>"
        yield (pagename, context, "page.html")


# add tags to page context
def add_tags(app, pagename, templatename, context, doctree):
    env = app.builder.env

    # add all tags associated with this page to the context
    if pagename in env.blog_posts:
        context["post_tags"] = [(tinkerer.utils.filename_from_title(tag), tag)
                for tag in env.blog_metadata[pagename].tags]


# setup tags
def setup(app):
    app.add_directive("tags", TagsDirective)

    app.connect("builder-inited", initialize)
    app.connect("html-collect-pages", make_tag_pages)
    app.connect("html-page-context", add_tags)


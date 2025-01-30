from markdown import Extension

from osbot_markdown.markdown.md__pre_processors.Pre_Processor__Chat_Bot import Pre_Processor__Chat_Bot


class Extension__Chat_Bot(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(Pre_Processor__Chat_Bot(md), 'chatbot', 175)
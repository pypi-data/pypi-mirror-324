from markdown.extensions import Extension

from osbot_markdown.markdown.md__patterns.Pattern__Video import Pattern__Video

VIDEO_RE = r'\[video:(.*?)(?:\|(.*?))?\]'
DEFAULT_VIDEO_WIDTH = '500'

class Extension__Video(Extension):
    def extendMarkdown(self, md):
        video_pattern = Pattern__Video(VIDEO_RE, self.getConfigs())
        md.inlinePatterns.register(video_pattern, 'video', 175)

    def __repr__(self):
        return f'VideoExtension'

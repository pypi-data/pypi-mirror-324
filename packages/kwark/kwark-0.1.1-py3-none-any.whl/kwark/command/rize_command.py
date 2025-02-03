from wizlib.parser import WizParser

from kwark.command import KwarkCommand
from kwark.util import load_prompt
from kwark.ai import AI


class RizeCommand(KwarkCommand):
    """Summarize observations and conclusions from random text such as a
    thread, email, or notes"""

    name = 'rize'
    prompt = load_prompt(name)

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        # parser.add_argument()

    def handle_vals(self):
        super().handle_vals()
        # if not self.provided('dir'):
        #     self.dir = self.app.config.get('filez4eva-source')

    @KwarkCommand.wrap
    def execute(self):
        input = self.app.stream.text
        prompt = self.prompt.format(text=input)
        response = AI().query(prompt)
        return response
        # return f"Hello, {input}!"

from anthropic import Anthropic


class AI:  # pragma: nocover

    model = 'claude-3-5-sonnet-20241022'

    def __init__(self):
        self.client = Anthropic()

    def query(self, text):
        """Send a one-time query, no tools"""
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }

        ]
        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=0,
            messages=messages)
        response = message.content[0].text
        return response

from discordwebhook import Discord

class DiscordSender:
    def __init__(self, webhook, logger):
        self.client = Discord(url=webhook)
        self.logger = logger

    def execute(self, text, *, image=None):
        if not text:
            self.logger.error("No text")
        
        self.client.post(
            content=text,
            file={
                "test.png": image
            }
        )

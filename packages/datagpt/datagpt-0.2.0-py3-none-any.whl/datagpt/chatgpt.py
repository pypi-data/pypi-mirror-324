import openai

class GPT:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        self.thread = None  

    def set_assistant_id(self, id):
        self.set_assistant_id = id

    def new_chat_and_run(self, prompt=None):
        self.thread = self.client.beta.threads.create(
                messages=[
                {
                "role": "user",
                "content": prompt,
                }
            ]
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id, assistant_id=self.set_assistant_id
        )
        messages = list(self.client.beta.threads.messages.list(thread_id=self.thread.id, run_id=run.id))
        messages[0].content[0].text
        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        for annotation in annotations:
            message_content.value = message_content.value.replace(annotation.text, "")
        return message_content.value

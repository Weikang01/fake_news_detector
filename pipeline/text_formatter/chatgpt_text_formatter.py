from pipeline.config import *
import re

from langchain.output_parsers import StructuredOutputParser, ResponseSchema


class ChatGPTTextFormatter:
    def _text_handler(self, text):
        """
        sample input:

a string like this: "Output:
[
 {'Who': 'Governments and health organizations', 'What': 'Contain the virus, implement safety measures, and develop vaccines', 'Where': 'Across the globe', 'When': 'Initial outbreak in Wuhan, China', 'Why': 'Curbing the virus's transmission', 'How': 'Social distancing, mask mandates, and lockdowns', 'Whom': 'Researchers and medical professionals', 'Outlook': 'Hope for a way out of the crisis'},
 {'Who': 'Everyone', 'What': 'Stay informed through reliable sources, follow recommended guidelines, and support one another', 'When': 'Navigate these uncertain times', 'Outcome': 'Work towards a healthier and safer future'}
]"
        converse it to list of dict
        :param text:
        :return:
        """
        pattern = r'\[.*?\]'
        text = re.findall(pattern, text)[0]

        text = text.replace("[", "")
        text = text.replace("]", "")
        text = text.replace("'", "")
        text = text.replace(" ", "")
        text = text.replace("\n", "")

        # remove possible space between close curly bracket and comma
        pattern = r'}\s*,'
        text = re.sub(pattern, '},', text)


        text = text.split("},")

        # TODO: continue here






    def format(self, text):
        while True:
            # try converse response to list of string
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",  # Use "text-davinci-003" for GPT-3.5
                    prompt=f"extract all useful information from the text and store it as list of dict in Python, where each dict represent an info extracted from the source which contain following keys like who\where\when\why\whom etc, and value is the answer: \n\n" + text,
                    max_tokens=450  # Adjust as needed
                )
                print(response.choices[0].text)
                return
            except:
                continue


if __name__ == '__main__':
    text = f"""
        The world has been grappling with the challenges posed by the coronavirus pandemic. From the initial outbreak in Wuhan, China, to its rapid spread across the globe, the virus has led to significant changes in our daily lives. Governments and health organizations have been working tirelessly to contain the virus, implement safety measures, and develop vaccines.

        Social distancing, mask mandates, and lockdowns have become part of the new normal as we strive to curb the virus's transmission. Researchers and medical professionals have been collaborating to better understand the virus's behavior, mutations, and potential long-term effects on health.

        The pandemic has highlighted the importance of global cooperation and scientific advancements. The rapid development and distribution of vaccines have offered hope for a way out of the crisis. However, challenges remain, such as vaccine distribution, addressing vaccine hesitancy, and monitoring the emergence of new variants.

        While we navigate these uncertain times, it's crucial to stay informed through reliable sources, follow recommended guidelines, and support one another. Together, we can overcome the challenges posed by the coronavirus and work towards a healthier and safer future."

        Please note that this text is generated for illustrative purposes and may not reflect the most up-to-date information or accurate details about the coronavirus pandemic. Always refer to trusted sources for accurate and current information.
        """

    text_formatter = ChatGPTTextFormatter()
    print(text_formatter.format(text))

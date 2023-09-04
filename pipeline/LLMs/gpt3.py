from pipeline.config import *


class GPT3P5:
    def __init__(self):
        pass

    def get_keywords(self, document):
        while True:
            # try converse response to list of string
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",  # Use "text-davinci-003" for GPT-3.5
                    prompt="find 5 most appropriate keywords for the following text and return as a list of string in Python, every keyword must be one noun: \n\n" + document + "\n\nkeyword:",
                    max_tokens=50  # Adjust as needed
                )
                return response.choices[0].text.strip().split("\n")
            except:
                continue


if __name__ == '__main__':
    test_document = f"""
    The world has been grappling with the challenges posed by the coronavirus pandemic. From the initial outbreak in Wuhan, China, to its rapid spread across the globe, the virus has led to significant changes in our daily lives. Governments and health organizations have been working tirelessly to contain the virus, implement safety measures, and develop vaccines.

    Social distancing, mask mandates, and lockdowns have become part of the new normal as we strive to curb the virus's transmission. Researchers and medical professionals have been collaborating to better understand the virus's behavior, mutations, and potential long-term effects on health.

    The pandemic has highlighted the importance of global cooperation and scientific advancements. The rapid development and distribution of vaccines have offered hope for a way out of the crisis. However, challenges remain, such as vaccine distribution, addressing vaccine hesitancy, and monitoring the emergence of new variants.

    While we navigate these uncertain times, it's crucial to stay informed through reliable sources, follow recommended guidelines, and support one another. Together, we can overcome the challenges posed by the coronavirus and work towards a healthier and safer future."

    Please note that this text is generated for illustrative purposes and may not reflect the most up-to-date information or accurate details about the coronavirus pandemic. Always refer to trusted sources for accurate and current information.
    """

    response = openai.Completion.create(
        engine="text-davinci-003",  # Use "text-davinci-003" for GPT-3.5
        prompt="find 5 most appropriate keywords for the following text and return as a list of string in Python, every keyword must be one noun: \n\n" + test_document + "\n\nkeyword:",
        max_tokens=50  # Adjust as needed
    )

    print(response.choices[0].text.strip())

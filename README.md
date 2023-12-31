﻿# fake_news_detector

## How to Start

1. install dependencies
    ```shell
    pip install -r requirements.txt
    ```



## Project Structure

### Data Generation Structure

We need three LLMs for this project

1. a LLM to extract keywords from corpus
2. a LLM to generate formatted corpus
3. a LLM to determine whether news input is real or not based on the formatted documents provided by retrieval model

#### We can train one model to accomplish all three tasks

data types

* `<s>extract keywords from following corpus: ${corpus}\nkeywords are: [keyword1, keyword2,...]<\s>`
* `<s>converse following corpus into json`



Other than that, we have a retrieval model, it will be a Doc2Vec layer, we can implement it with TFIDF, sentence embedding or Doc2Vec library.

### Inference Structure

![](https://github.com/Weikang01/fake_news_detector/blob/master/images/project%20diagram.drawio.png)

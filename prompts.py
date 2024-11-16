import os

import redis
from langchain_cohere import ChatCohere
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore
from redisvl.query.filter import Tag
from sklearn.datasets import fetch_20newsgroups

os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


class Smart:
    def __init__(self):

        self.llm = ChatCohere(model="command-r-plus")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        config = RedisConfig(
            index_name="newsgroups",
            redis_client=redis.Redis(host="redis", port=6379),
            metadata_schema=[
                {"name": "category", "type": "tag"},
            ],
        )
        self.vector_store = RedisVectorStore(embeddings, config=config)

        categories = ["sci.space"]
        newsgroups = fetch_20newsgroups(
            subset="train",
            categories=categories,
            shuffle=True,
            random_state=42,
        )

        # Use only the first 250 documents
        texts = newsgroups.data[:250]
        metadata = [
            {"category": newsgroups.target_names[target]}
            for target in newsgroups.target[:250]
        ]

        self.vector_store.add_texts(texts, metadata)

        # Prompt
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "human",
                    """
                    You are a helpful assistant designed to provide informative and unbiased answers to questions.
                    Please use the provided context to answer the question accurately and concisely. If you cannot find a suitable answer, simply state "I couldn't find an answer to that."
                    Avoid making claims of certainty or providing opinions. Stick to factual information.
                    Please analyze the input and, if it's factually correct and it`s not a question, respond with "This statement is true."
                    When you answer a question, you don't have to say "This statement is true". Just answer the question.
                    Identify the overall tone of the question as positive, negative, or neutral. Additionally, classify the tone as formal or informal.
                    Question: {question}
                    Context: {context}
                    Answer:""",
                ),
            ]
        )

        self.update_brain()

    def update_brain(self):

        retriever = self.vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 2}
        )

        self.rag_chain = (
            {
                "context": retriever | self.format_docs,
                "question": RunnablePassthrough(),
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def reply(self, text):
        return self.rag_chain.invoke(text)

    def learn(self, text):
        metadata = [{"category": "sci.space"}, {"category": "User"}]
        texts = "From: User ! Subject: This is a User Statement ! Re: " + text
        document_1 = Document(page_content=texts, metadata=metadata[0])
        document_2 = Document(page_content=texts, metadata=metadata[1])

        self.vector_store.add_documents(documents=[document_1, document_2])
        self.update_brain()

    def search_user_statements(self):
        query = "User"
        results = self.vector_store.similarity_search(
            query,
            k=100,
            filter=Tag("category") == "User",
        )
        return [result.page_content for result in results]

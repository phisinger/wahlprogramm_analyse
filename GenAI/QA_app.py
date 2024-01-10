from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma
from Vectorstore import Vectorstore_client
import gradio as gr

# Load Model
from langchain.llms import GPT4All

llm = GPT4All(
    model="/home/phisinger/Programmieren/wahlprogramm_analyse/models/mistral-7b-openorca.Q4_0.gguf",
    max_tokens=2048,
)

# establish connection to vector store chroma
db_client = Vectorstore_client()
db_client = db_client.get_client()


collection_name = ""


with gr.Blocks() as demo:
    gr.Markdown("# Election Program Chatbot")

    def set_collection(year):
        global collection_name
        collection_name = year
    # Dropdown to select the year to ask
    gr.Interface(
        fn=set_collection,
        inputs=gr.Dropdown(
            ["2013", "2017", "2021"], label="Election Year", info="Select the election year you want to chat with"),
        outputs=None,
    )

    # Explain chatbot
    gr.Markdown(
        """The chatbot has access to all election programs of the selected year. You may ask questions in German. As this is a demo, you should be warned that the generation can take several minutes (up to 600 secs). <br/>
        Be also aware that the chatbot doesn't take into account the history of the chat. It answers every question independently.""")

    def generate_answer(message, history):
        global collection_name
        if collection_name == "":
            gr.Warning(
                "No election year is selected! The default year '2021' is used.")
            collection_name = "2021"
        # integrate vector store into langchain chroma version
        langchain_chroma = Chroma(
            client=db_client,
            collection_name=collection_name,
            embedding_function=GPT4AllEmbeddings(),
        )

        # Prepare chain to ask questions
        # german default prompt
        german_prompt = """Beantworten Sie die Frage am Ende des Textes anhand der folgenden Informationen. Wenn Sie die Antwort nicht wissen, sagen Sie einfach, dass Sie es nicht wissen, versuchen Sie nicht, eine Antwort zu erfinden.

        {context}

        Frage: {question}
        Hilfreiche Antwort:"""
        german_prompt = PromptTemplate(
            template=german_prompt, input_variables=["context", "question"]
        )

        # TODO: Make Prompt for Wahlomat-like usage

        # create Q & A chain for the chatbot
        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=langchain_chroma.as_retriever(),
            chain_type_kwargs={"prompt": german_prompt},
        )

        return qa_chain({"query": message})["result"]
    gr.ChatInterface(generate_answer)


demo.launch()

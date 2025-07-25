import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
import torch
import base64
import textwrap
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA

# ----------------------------------------------------------
# Author: Arpita
# GitHub: https://github.com/Arpitaa19/QueryDoc-AI
# Description: Generative AI-powered PDF Q&A App
# ----------------------------------------------------------

# model and tokenizer loading
checkpoint = "MBZUAI/LaMini-T5-738M"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelForSeq2SeqLM.from_pretrained(
    checkpoint, 
    device_map='cpu', 
    torch_dtype=torch.float32,
    low_cpu_mem_usage=True,
    # offload_folder="./offload" 
)

# Print the device mapping after loading the model
print("Device mapping:", base_model.hf_device_map)


@st.cache_resource
def llm_pipeline():
    pipe = pipeline(
        'text2text-generation',
        model=base_model,
        tokenizer=tokenizer,
        max_length=256,
        do_sample=True,
        temperature=0.3,
        top_p=0.95
    )
    local_llm = HuggingFacePipeline(pipeline=pipe)
    return local_llm


@st.cache_resource
def qa_llm():
    llm = llm_pipeline()
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="db", embedding_function=embeddings)
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
    return qa


def process_answer(instruction):
    response = ''
    instruction = instruction
    qa = qa_llm()
    generated_text = qa(instruction)
    answer = generated_text['result']
    return answer, generated_text


def main():
    st.title("QueryDoc AI")
    with st.expander("About the App"):
        st.markdown(
            """
            This is a Generative AI-powered app that answers questions about your PDF file using LaMini-T5 and LangChain.
            """
        )
    question = st.text_area("Enter your Question")
    if st.button("Ask"):
        st.info("Your Question: " + question)
        with st.spinner("Generating answer..."):
            answer, metadata = process_answer(question)
        st.info("Your Answer")
        st.write(answer)
        st.write(metadata)


if __name__ == '__main__':
    main()

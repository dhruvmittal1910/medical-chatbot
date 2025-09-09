# here we will be using flask backend

from flask import Flask, render_template, jsonify,request
from src.helper import download_embedding_model
import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import prompt_template
from flask_cors import CORS


load_dotenv()

app=Flask(__name__)
CORS(app)


PINECONE_API_KEY=os.getenv('PINECONE_API_KEY')
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

os.environ['PINECONE_API_KEY']=PINECONE_API_KEY
os.environ['OPENAI_API_KEY']=OPENAI_API_KEY


# load the mebedding model
embeddings=download_embedding_model()

index_name="medical-chatbot"

# loading the existing index
# embed each chunk and upsert the embeddings into your pinecone index
docSearch=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# here if you want you can additional documnets inputed by user to increase the knowledge base
"""dummy=Document(
    page_content='Lionel Messi is the best soccer player',
    metadata={'source':'manual_entry'}
)
docSearch.add_documents([dummy])"""

# create the chain
retriever=docSearch.as_retriever(
    search_type='similarity',
    search_kwargs={"k":4}, # overlapping chunks number, get top 4 retrived sentences
)

chatmodel=ChatOpenAI(
    model='gpt-4o'
)

# create a chain, to setup the rag pipleine
# ChatPromptTemplate = defines how to ask

# create_stuff_documents_chain = defines how to insert docs into the prompt

# create_retrieval_chain = glues retriever + doc chain into a single RAG pipeline


prompt=ChatPromptTemplate.from_messages( # Use from_messages for multiple roles

        [ # Pass a list of tuples
            ("system",prompt_template), #the system prompt
            ("human","{input}") #input from the user
        ]

)


question_answer_chain=create_stuff_documents_chain(chatmodel,prompt)
rag_chain=create_retrieval_chain(retriever,question_answer_chain)




@app.route("/")
def index():
    # render the react app
    return render_template('chat.html')

# for html
@app.route("/get",methods=['GET','POST'])
def chat():
    data=request.form['msg']
    input=data
    print("user input --- ",input)
    response=rag_chain.invoke({"input":input})
    print("bot response---", response)
    return str(response['answer'])


# route for sending the message

# for react

# @app.route("/get",methods=['GET','POST'])
# def chat():
#     data=request.get_json()
#     input=data['msg']
#     print("user input --- ",input)
#     response=rag_chain.invoke({"input":input})
#     print("bot response---", response)
#     return jsonify(response['answer'])

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080,debug=True)
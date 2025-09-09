import os
from pinecone import Pinecone
from pinecone import ServerlessSpec
from src.helper import extract_pdf_files,filter_extracted_data,text_splitter,download_embedding_model
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

from dotenv import load_dotenv
load_dotenv()

PINECONE_API_KEY=os.getenv('PINECONE_API_KEY')
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

os.environ['PINECONE_API_KEY']=PINECONE_API_KEY
os.environ['OPENAI_API_KEY']=OPENAI_API_KEY



extracted_data=extract_pdf_files(data_path='data/')
print(len(extracted_data))
# the extracted data has a lot of content, i only need page content and metadata that wil be source in my case
filtered_data=filter_extracted_data(extracted_data)

# perform chunking on the filtered data
text_chunks=text_splitter(filtered_data)

# do embeddings of the chunks 
embeddings=download_embedding_model()


# create a pinecone client
pinecone_client=Pinecone(
    api_key=PINECONE_API_KEY
)

# now create the index or database to store the embeddings
index_name='medical-chatbot'

if not pinecone_client.has_index(index_name):
    # mneans the database not present so create one
    pinecone_client.create_index(
        name=index_name,
        dimension=384, # dimenstion of the embeddings that we got above
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index=pinecone_client.Index(index_name)

# creating embeddings using hf sentence transformer
docSearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings
)



# creating a dummy documnet
dummy=Document(
    page_content='Lionel Messi is the best soccer player',
    metadata={'source':'manual_entry'}
)

# if we want to add more data t the existing pinecone index to increase the kb
"""docSearch.add_documents([dummy])""" #with this you can do


print(docSearch.add_documents([dummy]))
# if we want to load a exisiting index and continue the work
"""# from langchain_pinecone import PineconeVectorStore

# existing_docSearch=PineconeVectorStore.from_existing_index(
#     index_name=index_name,
#     embedding=embeddings,
# )
"""



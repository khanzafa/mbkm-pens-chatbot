import dotenv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

MAGANG_CSV_PATH = "data/magang_mbkm.csv"
CHROMA_PATH = "chroma_data"

dotenv.load_dotenv()

# Load CSV file with UTF-8 encoding
loader = CSVLoader(file_path=MAGANG_CSV_PATH, encoding='utf-8', source_column="Pesan")
reviews = loader.load()

reviews_vector_db = Chroma.from_documents(
    reviews, GoogleGenerativeAIEmbeddings(model="models/embedding-001"), persist_directory=CHROMA_PATH
)

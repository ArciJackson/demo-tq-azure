import logging
import azure.functions as func
from azure.search.documents import SearchClient, IndexDocumentsBatch, IndexAction
from azure.storage.blob import BlobServiceClient
import PyPDF2

def main(req: func.HttpRequest) -> func.HttpResponse:
    file = req.files.get('pdf')
    if not file:
        return func.HttpResponse("Por favor, suba un archivo PDF.", status_code=400)

    content = extract_text_from_pdf(file)
    document = {
        "id": file.filename,
        "content": content,
        "filename": file.filename,
        "upload_date": datetime.utcnow().isoformat()
    }

    search_client = get_search_client()
    batch = IndexDocumentsBatch(actions=[IndexAction(action_type="upload", document=document)])
    search_client.index_documents(batch)

    return func.HttpResponse("Documento indexado exitosamente.", status_code=201)

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = "".join(page.extract_text() for page in pdf_reader.pages)
    return text

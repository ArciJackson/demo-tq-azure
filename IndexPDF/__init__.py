import logging
import azure.functions as func
from azure.search.documents import SearchClient, IndexDocumentsBatch, IndexAction
import PyPDF2

def main(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == 'POST':
        file = req.files.get('pdf')
        if not file:
            return func.HttpResponse("Por favor, suba un archivo PDF.", status_code=400)

        content = extract_text_from_pdf(file)
        document = {
            "id": file.filename,
            "content": content,
            "filename": file.filename
        }

        search_client = get_search_client()
        batch = IndexDocumentsBatch(actions=[IndexAction(action_type="upload", document=document)])
        search_client.index_documents(batch)

        return func.HttpResponse("Documento indexado exitosamente.", status_code=201)

    if req.method == 'GET':
        query = req.params.get('q')
        if not query:
            return func.HttpResponse("Por favor, proporcione un término de búsqueda.", status_code=400)

        search_client = get_search_client()
        results = search_client.search(query)
        response = [doc['content'] for doc in results]

        return func.HttpResponse(str(response), status_code=200)

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = "".join(page.extract_text() for page in pdf_reader.pages)
    return text

def get_search_client():
    return SearchClient(endpoint="<tu-endpoint-de-search>", index_name="<tu-índice>", credential="<tu-credential>")

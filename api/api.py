from io import StringIO
from io import BytesIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from flask import send_file, send_from_directory, safe_join, abort

import gtts
from flask import Flask
from flask import request

from flask_cors import CORS
from flask_cors import CORS, cross_origin
from flask import jsonify

app = Flask(__name__)
cors = CORS(app)
app.config['Content-Type'] = 'multipart/form-data'

CORS(app, resources={r"/*": {"origins": "*"}})
@cross_origin()

@app.route('/', methods=['GET', 'POST'])
def hello():
    return "Standard route test"

@app.route('/tes1', methods=['GET', 'POST'])
def hel():
    return "Parameter test on the route"

@app.route('/pdf_normal', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()

def upload_file():
    if request.method == 'POST':
        output_string = StringIO()
        in_file = request.files["file"]
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        texto = output_string.getvalue()
        # Gerando mp3
        tts = gtts.gTTS(texto,  lang="pt-br")
        mp3_fp = BytesIO()
        # tts.write_to_fp(mp3_fp)
        tts.save('mp3_fp.mp3')
        response = jsonify(message="Simple server is running")
        response.headers.add("Access-Control-Allow-Origin", "*")

        return send_file('mp3_fp.mp3', as_attachment=True)
    else:
        return "Method POST not found"


CORS(app.run())
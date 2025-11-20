from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from lxml import etree

app = Flask(__name__)
CORS(app)

@app.route('/transform', methods=['POST'])
def transform():
    if 'xml' not in request.files or 'xslt' not in request.files:
        return jsonify({"error": "Missing XML or XSLT file"}), 400

    xml_file = request.files['xml']
    xslt_file = request.files['xslt']
    output_format = request.form.get('outputFormat', 'xml')

    try:
        xml_tree = etree.parse(xml_file)
        xslt_tree = etree.parse(xslt_file)
        transform = etree.XSLT(xslt_tree)
        result = transform(xml_tree)

        content_type = {
            'xml': 'application/xml',
            'html': 'text/html',
            'text': 'text/plain'
        }.get(output_format, 'application/xml')

        return Response(str(result), content_type=content_type)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()

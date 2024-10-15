from flask import Flask, request
from sqlalchemy import create_engine
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)

@app.route('/healthz', methods=['GET'])
def health_check():
    # If payload is sent in request then 400:Bad Request
    if request.content_length:
        return '', 400
    
    try:
        # If db connection successful then 200: OK 
        db_conn = db_engine.connect()
        db_conn.close()
        return '', 200, {'Cache-Control': 'no-cache, no-store, must-revalidate'}
    except Exception as e:
        return '', 503, {'Cache-Control': 'no-cache, no-store, must-revalidate'}
    

@app.route('/healthz', methods=["POST", "PUT", "DELETE", "PATCH"])
def invalid_method():
    return '', 405, {'Cache-Control': 'no-cache, no-store, must-revalidate'}

if __name__ == '__main__':
    app.run(debug=True)
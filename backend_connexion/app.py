import connexion
from flask_cors import CORS
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create Connexion app
app = connexion.App(__name__, specification_dir=".")
app.add_api("openapi.yaml", 
           strict_validation=True, 
           validate_responses=True,
           options={"swagger_ui": True, "serve_spec": True})
CORS(app.app)  # Enable CORS for all routes
application = app.app

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")

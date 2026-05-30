from flask import Flask
from models.air_quality import AirQualityMonitor
from routes.main_routes import create_main_routes
from routes.compare_routes import create_compare_routes
from routes.sort_routes import create_sort_routes
from routes.graph_routes import create_graph_routes
from routes.auth_routes import create_auth_routes

app = Flask(__name__)
app.secret_key = 'super-secret-key-123'

app.config['SESSION_PERMANENT'] = False

monitor = AirQualityMonitor()

app.register_blueprint(create_main_routes(monitor))
app.register_blueprint(create_compare_routes(monitor))
app.register_blueprint(create_sort_routes(monitor))
app.register_blueprint(create_graph_routes(monitor))
app.register_blueprint(create_auth_routes(monitor))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
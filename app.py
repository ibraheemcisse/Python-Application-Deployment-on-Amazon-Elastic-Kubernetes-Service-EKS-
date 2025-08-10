#!/usr/bin/env python3
"""
Enhanced Flask Application for EKS Deployment
Includes health checks, metrics, and production-ready features.
"""

import os
import time
import logging
import threading
from datetime import datetime
from flask import Flask, jsonify, request, render_template_string
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/var/log/flask-app.log') if os.path.exists('/var/log') else logging.NullHandler()
    ]
)

logger = logging.getLogger(__name__)

# Application metrics
class AppMetrics:
    def __init__(self):
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0
        self.lock = threading.Lock()
    
    def increment_requests(self):
        with self.lock:
            self.request_count += 1
    
    def increment_errors(self):
        with self.lock:
            self.error_count += 1
    
    def get_uptime(self):
        return time.time() - self.start_time
    
    def get_stats(self):
        return {
            'uptime_seconds': self.get_uptime(),
            'total_requests': self.request_count,
            'total_errors': self.error_count,
            'memory_usage_mb': psutil.Process().memory_info().rss / 1024 / 1024,
            'cpu_percent': psutil.Process().cpu_percent()
        }

# Initialize Flask app and metrics
app = Flask(__name__)
metrics = AppMetrics()

# Configuration
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-change-in-production'),
    DEBUG=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true',
    TESTING=False
)

# Request middleware for metrics
@app.before_request
def before_request():
    request.start_time = time.time()
    metrics.increment_requests()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    logger.info(f"{request.method} {request.path} - {response.status_code} - {duration:.3f}s")
    return response

@app.errorhandler(500)
def handle_500(error):
    metrics.increment_errors()
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end',
        'timestamp': datetime.utcnow().isoformat()
    }), 500

@app.errorhandler(404)
def handle_404(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found',
        'timestamp': datetime.utcnow().isoformat()
    }), 404

# HTML template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask App on EKS</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .metrics { background: #ecf0f1; padding: 15px; border-radius: 4px; margin: 20px 0; }
        .endpoint { background: #e8f5e8; padding: 10px; margin: 10px 0; border-left: 4px solid #27ae60; }
        .status-ok { color: #27ae60; font-weight: bold; }
        .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">🚀 Flask Application on Amazon EKS</h1>
        
        <div class="info-grid">
            <div>
                <h3>Application Status</h3>
                <p class="status-ok">✅ Running Successfully</p>
                <p><strong>Version:</strong> {{ version }}</p>
                <p><strong>Environment:</strong> {{ environment }}</p>
                <p><strong>Pod Name:</strong> {{ pod_name }}</p>
            </div>
            
            <div>
                <h3>Runtime Info</h3>
                <p><strong>Uptime:</strong> {{ uptime }} seconds</p>
                <p><strong>Memory Usage:</strong> {{ memory_mb }} MB</p>
                <p><strong>CPU Usage:</strong> {{ cpu_percent }}%</p>
                <p><strong>Total Requests:</strong> {{ total_requests }}</p>
            </div>
        </div>
        
        <div class="metrics">
            <h3>📊 Available Endpoints</h3>
            <div class="endpoint"><strong>GET /</strong> - This home page</div>
            <div class="endpoint"><strong>GET /health</strong> - Health check endpoint</div>
            <div class="endpoint"><strong>GET /ready</strong> - Readiness probe endpoint</div>
            <div class="endpoint"><strong>GET /metrics</strong> - Application metrics (JSON)</div>
            <div class="endpoint"><strong>GET /info</strong> - System information (JSON)</div>
            <div class="endpoint"><strong>POST /echo</strong> - Echo service for testing</div>
        </div>
        
        <div class="metrics">
            <h3>🔧 Kubernetes Integration</h3>
            <p>This application includes:</p>
            <ul>
                <li>Health checks for Kubernetes probes</li>
                <li>Graceful shutdown handling</li>
                <li>Resource monitoring and metrics</li>
                <li>Proper logging for observability</li>
                <li>Security context compliance</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

# Routes
@app.route('/')
def home():
    """Main application page with status information"""
    try:
        stats = metrics.get_stats()
        return render_template_string(HOME_TEMPLATE,
            version=os.environ.get('APP_VERSION', '1.0.0'),
            environment=os.environ.get('FLASK_ENV', 'production'),
            pod_name=os.environ.get('HOSTNAME', 'unknown'),
            uptime=f"{stats['uptime_seconds']:.1f}",
            memory_mb=f"{stats['memory_usage_mb']:.1f}",
            cpu_percent=f"{stats['cpu_percent']:.1f}",
            total_requests=stats['total_requests']
        )
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        return jsonify({'error': 'Failed to render page'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for Kubernetes liveness probe"""
    try:
        # Perform basic health checks
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': os.environ.get('APP_VERSION', '1.0.0'),
            'uptime_seconds': metrics.get_uptime()
        }
        
        # You can add more health checks here:
        # - Database connectivity
        # - External service availability
        # - Disk space checks
        
        return jsonify(health_status), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503

@app.route('/ready')
def readiness_check():
    """Readiness check endpoint for Kubernetes readiness probe"""
    try:
        # Check if application is ready to serve traffic
        ready_status = {
            'status': 'ready',
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {
                'application': 'ok',
                'dependencies': 'ok'  # Add external dependency checks here
            }
        }
        
        return jsonify(ready_status), 200
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return jsonify({
            'status': 'not_ready',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503

@app.route('/metrics')
def metrics_endpoint():
    """Metrics endpoint for monitoring systems"""
    try:
        stats = metrics.get_stats()
        
        # Add application-specific metrics
        app_metrics = {
            'application': {
                'name': 'flask-eks-app',
                'version': os.environ.get('APP_VERSION', '1.0.0'),
                'environment': os.environ.get('FLASK_ENV', 'production')
            },
            'runtime': stats,
            'system': {
                'hostname': os.environ.get('HOSTNAME', 'unknown'),
                'platform': os.name,
                'python_version': os.sys.version.split()[0]
            },
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(app_metrics), 200
    except Exception as e:
        logger.error(f"Metrics endpoint failed: {e}")
        return jsonify({'error': 'Failed to retrieve metrics'}), 500

@app.route('/info')
def info():
    """System information endpoint"""
    try:
        system_info = {
            'hostname': os.environ.get('HOSTNAME', 'unknown'),
            'pod_ip': os.environ.get('POD_IP', 'unknown'),
            'node_name': os.environ.get('NODE_NAME', 'unknown'),
            'namespace': os.environ.get('POD_NAMESPACE', 'unknown'),
            'service_account': os.environ.get('SERVICE_ACCOUNT', 'unknown'),
            'app_version': os.environ.get('APP_VERSION', '1.0.0'),
            'build_date': os.environ.get('BUILD_DATE', 'unknown'),
            'git_commit': os.environ.get('GIT_COMMIT', 'unknown')
        }
        
        return jsonify(system_info), 200
    except Exception as e:
        logger.error(f"Info endpoint failed: {e}")
        return jsonify({'error': 'Failed to retrieve system info'}), 500

@app.route('/echo', methods=['POST'])
def echo():
    """Echo service for testing POST requests"""
    try:
        data = request.get_json() or {}
        
        response = {
            'echo': data,
            'method': request.method,
            'headers': dict(request.headers),
            'timestamp': datetime.utcnow().isoformat(),
            'client_ip': request.remote_addr
        }
        
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Echo endpoint failed: {e}")
        metrics.increment_errors()
        return jsonify({'error': 'Failed to process request'}), 500

@app.route('/simulate-error')
def simulate_error():
    """Endpoint to simulate errors for testing"""
    if app.config.get('DEBUG'):
        raise Exception("Simulated error for testing")
    else:
        return jsonify({'error': 'Error simulation disabled in production'}), 403

# Graceful shutdown handler
def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}. Shutting down gracefully...")
    # Perform cleanup tasks here
    logger.info("Application shutdown complete")

if __name__ == '__main__':
    import signal
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Get configuration from environment
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask application on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'production')}")
    
    try:
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True,
            use_reloader=False  # Disable reloader in container
        )
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

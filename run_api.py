"""Run the Timeseries SVG API server."""

import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("Timeseries SVG API Server")
    print("=" * 60)
    print("API Documentation: http://localhost:9300/docs")
    print("Health Check: http://localhost:9300/health")
    print("Landing Page: http://localhost:9300/")
    print("=" * 60)
    
    uvicorn.run("timeseries_svg.api:create_app", host="0.0.0.0", port=9300, reload=True)

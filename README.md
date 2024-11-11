# Patent Infringement Checker

A Flask API for checking potential patent infringements by analyzing company products and patents.

## Requirements

- **Python**: 3.10 (or use Docker)
- **Flask** with CORS support

## Endpoints

1. **`POST /api/analyze`**
   - **Description**: Analyzes a patent for infringement based on company data.
   - **Request Body**:
     ```json
     {
       "patent_id": "<PATENT_ID>",
       "company_name": "<COMPANY_NAME>"
     }
     ```
   - **Response**: JSON with analysis details or an error message.

2. **`GET /api/test`**
   - **Description**: Test endpoint to verify API functionality.
   - **Response**: `{"message": "API is working!"}`

## Docker Deployment

### Load and Run the Docker Image (from ZIP file)

If you received a zipped Docker image file, follow these steps to load and run the application:

1. **Unzip the Docker Image**:
   - Extract the `flask-app.tar` file from the zip archive you received.

2. **Load the Docker Image**:
   - Open a terminal and load the image using the `docker load` command:
     ```bash
     docker load -i flask-app.tar
     ```

3. **Run the Docker Container**:
   - Start the container, mapping port 5000 to access the app locally:
     ```bash
     docker run -p 5000:5000 flask-app
     ```

4. **Access the Application**:
   - Go to [http://localhost:5000](http://localhost:5000) in your browser to access the API.


## Quick Start (Run Locally without Docker)

1. Clone the repo and navigate to the directory:
   ```bash
   git clone https://github.com/gjeng7/patent_infringement_checker.git
   cd patent_infringement_checker
   ```
2. Create a virtual environment and install dependencies:
   ```bash
    python3.10 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
3. Run the app:
    ```bash
    export FLASK_APP=app/main.py
    flask run
    ```
4. Test in your browser or with curl:
    ```bash 
    curl http://localhost:5000/api/test
    ```
## Build Docker Image Manually

1. Build the Docker Image
    ```bash
    docker build -t flask-app .
    ```
2. Run the Docker Container:
    ```bash 
    docker run -p 5000:5000 flask-app
    ```
3. Access the app at http://localhost:5000.

## Run the UI 
1. Go into the UI folder, and then into the patent infringement checker front end folder
2. Use ```npm start``` to run the UI 





# HTML to PDF Microservice

This project is a Python-based microservice that generates PDF files from HTML templates. It uses FastAPI for handling HTTP requests and WeasyPrint for generating PDFs.

## Features

- Accepts HTTP POST requests with data in JSON format.
- Dynamically generates HTML using Jinja2 templates.
- Converts the generated HTML into a PDF file.
- Returns the PDF as a downloadable response.

## Requirements

- Python 3.7 or higher
- Dependencies specified in `requirements.txt`

## Setup

1. Clone this repository and navigate to the project folder.

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\\Scripts\\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
html-to-pdf-python/
├── main.py              # Main FastAPI application file
├── requirements.txt     # List of Python dependencies
├── templates/           # Folder containing HTML templates
│   └── example.html     # Example of template
└── readme.md            # Project documentation
```

## How to Run

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API documentation at:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoints

### `POST /generate-pdf/`

- **Description**: Generates a PDF from the provided data.
- **Request Body**:
  ```json
    {
    "data": {
        "work_order_id": "2399",
            "date": "2024-12-08",
            "customer": "MATCOT CIA LTDA",
            "plate": "AAA-4598",
            "model": "P460",
            "chassis": "3939547",
            "description": "Reemplazo de filtros de aire\nReemplazo de solenoide de APS\nReemplazo de filtro de secador",
            "spareList": [
                {"code": "2277576", "description": "Kit de mantenimientos", "quantity": "1"},
                {"code": "1381235", "description": "Filtro de retardador", "quantity": "1"}
            ]
        }
    }
  ```
- **Response**: Returns a PDF file as a downloadable stream.

The command generates a `report.pdf` file in the current directory.

## Notes

- Ensure that the `templates/example.html` file exists and is properly formatted for rendering.
- You can modify the `example.html` template to customize the PDF layout and design.

## License

This project is licensed under the MIT License.
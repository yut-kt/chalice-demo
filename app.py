"""Chalice app."""
import csv
import io
from cgi import FieldStorage

from chalice import BadRequestError, Chalice, Response

app = Chalice(app_name="chalice-demo")
app.api.binary_types.append("multipart/form-data")


@app.route("/")
def index() -> Response:
    """Index route."""
    return Response(body={"hello": "world"})


@app.route("/csv", methods=["POST"], content_types=["multipart/form-data"])
def upload_csv() -> Response:
    """Upload CSV route."""
    fp = io.BytesIO(app.current_request.raw_body)
    fs = FieldStorage(fp=fp, environ={"REQUEST_METHOD": "POST"}, headers=app.current_request.headers)

    csv_content = fs.getvalue("csv_file")
    try:
        csv_str = csv_content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            csv_str = csv_content.decode("shift_jis")
        except UnicodeDecodeError:
            msg = "CSV encoding must be UTF-8 or Shift_JIS."
            raise BadRequestError(msg) from UnicodeDecodeError

    csv_reader = csv.DictReader(io.StringIO(csv_str))
    csv_rows = list(csv_reader)
    csv_rows.append({"name": "user99", "display_name": "User ９９", "email": "user99@example.com"})

    response_csv = io.StringIO()
    csv_writer = csv.DictWriter(response_csv, fieldnames=["name", "display_name", "email"])
    csv_writer.writeheader()
    csv_writer.writerows(csv_rows)

    return Response(body=response_csv.getvalue().strip().encode(fs.getvalue("encoding", "utf-8")),
                    headers={"Content-Type": "text/csv"})

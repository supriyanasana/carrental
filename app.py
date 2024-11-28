from flask import Flask, render_template, request
from azure.storage.blob import BlobServiceClient
import mysql.connector  # Use mysql.connector for MySQL database

app = Flask(__name__)

# Azure Blob Storage connection
BLOB_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=carrentalazure;AccountKey=NdhMVwvEBT78MA4Xy9bLJelBjkOIqj/UtfR7TB3OOiHJw//mojDBDJ6jYzYMR6I3I1zYCDihmlQK+AStmxdRaA==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=carrentalazure;AccountKey=NdhMVwvEBT78MA4Xy9bLJelBjkOIqj/UtfR7TB3OOiHJw//mojDBDJ6jYzYMR6I3I1zYCDihmlQK+AStmxdRaA==;EndpointSuffix=core.windows.net")
container_name = "car-images"

# MySQL Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',  # MySQL server hostname (use 'localhost' for local MySQL)
        user='root',       # MySQL username
        password='supriya123',  # Your MySQL password
        database='CarRentalUsers'   # The database you created
    )
    return conn

@app.route("/")
def home():
    # Fetch car details from Blob Storage
    container_client = blob_service_client.get_container_client('car-images')
    blobs = container_client.list_blobs()
    cars = [{"name": blob.name, "url": f"https://carrentalazure.blob.core.windows.net/{'car-images'}/{blob.name}"} for blob in blobs]
    return render_template("index.html", cars=cars)

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (Username, Email, Password) VALUES (%s, %s, %s)", (username, email, password))
    conn.commit()
    cursor.close()
    conn.close()

    return "Registration Successful!"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)


import pyodbc
import plotly.graph_objs as go
import plotly.offline as opy
from flask import Flask, render_template


# Connect to the Azure SQL database
conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                      'SERVER=tcp:finalprojectanalysis1.database.windows.net,1433;'
                      'DATABASE=redditanalysis;'
                      'UID=EDMGroup;'
                      'PWD=Projectanalysis3;'
                      'Encrypt=yes;'
                      'TrustServerCertificate=no;'
                      'Connection Timeout=30;')

# Create a cursor object
cursor = conn.cursor()

# Create a Flask app instance
app = Flask(__name__)

# Define a route for the home page ('/') and a function that retrieves the data from the database and renders a template
@app.route('/')
def display_data():
    # Execute a SQL query to get the sentiment counts
    cursor.execute('SELECT Sentiment, COUNT(*) AS Count FROM SentimentAnalysis GROUP BY Sentiment')


    # Fetch all the rows from the query result
    rowsone = cursor.fetchall()
    # Extract the sentiment labels and counts from the rows
    sentiments = [row[0] for row in rowsone]
    counts = [row[1] for row in rowsone]
    # Create a Plotly pie chart
    data = [go.Pie(labels=sentiments, values=counts)]
    chart_div = opy.plot(data, auto_open=False, output_type='div')
    
    # Execute a SQL query to get the table data
    cursor.execute('SELECT * FROM SentimentAnalysis')
    # Fetch the top 10 rows from the query result
    rows = cursor.fetchmany(10)

    cursor.execute('SELECT Score, Headline FROM SentimentAnalysis ORDER BY Score')

    # Render the template with the data
    rowstwo = cursor.fetchall()

    scores = [row[1] for row in rowstwo]
    comments = [row[0] for row in rowstwo]

    data2 = [go.Bar(x=scores, y=comments)]
    chart_div2 = opy.plot(data2, auto_open=False, output_type='div')

    
    # Render the template with the data
    # Render the template with the data
    return render_template('data.html', rows=rows, chart_div=chart_div, chart_div2=chart_div2)

@app.route('/table.html')
def display_table():
    # Execute a SQL query to get all the data from the SentimentAnalysis table
    cursor.execute('SELECT * FROM SentimentAnalysis')
    # Fetch all the rows from the query result
    rows = cursor.fetchall()

    # Render the template with the data
    return render_template('table.html', rows=rows)


# Run the Flask app
if __name__ == '__main__':
    app.run()

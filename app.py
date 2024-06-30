from flask import Flask, render_template, request, send_file, send_from_directory
import os
from utils.utils import app_gen, exp1, exp2, exp3, exp4
import pandas as pd
import io

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    option = request.form['options']
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        # Read the uploaded file as a binary stream
        file_stream = io.BytesIO(file.read())
        df = pd.read_csv(file_stream, delimiter=',', header=None)
        results = []
        for column in df.columns:
            col_values = df[column].values
            if len(col_values) >= 5:
                if option == 'exp1':
                    result = exp1(col_values[:5])
                elif option == 'exp2':
                    result = exp2(col_values[:5])
                elif option == 'exp3':
                    result = exp3(col_values[:5])
                elif option == 'exp4':
                    result = exp4(col_values[:5])
                elif option == 'app_gen':
                    result = app_gen(col_values[:5])
                else:
                    return "Invalid request"
                results.append(result)
        results_df = pd.DataFrame([results])
        results_csv_stream = io.StringIO()
        results_df.to_csv(results_csv_stream, index=False, header=False)
        results_csv_stream.seek(0)
        return send_file(
            io.BytesIO(results_csv_stream.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{option}.csv'
        )

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
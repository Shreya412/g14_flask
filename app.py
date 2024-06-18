from flask import Flask, render_template, request, send_file, send_from_directory
import os
from utils.utils import app_gen, exp1, exp2, exp3, exp4  # Adjust import as necessary
import pandas as pd

app = Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    requests = request.form['options']
    print(requests, "request")
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(filename, "::::")

        # Read the uploaded file
        df = pd.read_csv(file_path, delimiter=',', header=None)

        # Process the file
        results = []
        for column in df.columns:
            col_values = df[column].values
            if len(col_values) >= 5:
                if requests == 'exp1':
                    result = exp1(col_values[:5])
                elif requests == 'exp2':
                    result = exp2(col_values[:5])
                elif requests == 'exp3':
                    result = exp3(col_values[:5])
                elif requests == 'exp4':
                    result = exp4(col_values[:5])
                elif requests == 'app_gen':
                    result = app_gen(col_values[:5])
                else:
                    return "Invalid request"
                results.append(result)
        
        # Create results DataFrame
        results_df = pd.DataFrame([results])
        results_csv_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{requests}.csv')
        results_df.to_csv(results_csv_path, index=False, header=False)
        print(f"Results saved to '{requests}.csv'.")

        # Send the results file
        return send_file(results_csv_path, as_attachment=True)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

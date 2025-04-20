import os
import pandas as pd 
from  flask import Flask, render_template, request, send_file

app = Flask(__name__)

DATA_FILE = 'data.csv'

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            likes = int(request.form["likes"])
            comments = int(request.form["comments"])
            followers = int(request.form["followers"])

            df = pd.DataFrame([{
                "likes": likes,
                "comments": comments,
                "followers": followers
            }])

            df["engagement_rate"] = ((df["likes"] + df["comments"]) / df["followers"]) * 100
            result = round(df["engagement_rate"].iloc[0], 1)

            df["engagement_rate"] = result

            if os.path.exists(DATA_FILE):
                df_existing = pd.read_csv(DATA_FILE)
                df = pd.concat([df_existing, df], ignore_index=True)

            df.to_csv(DATA_FILE, index=False)

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result)

@app.route("/download")
def download_excel():
    try:
        df = pd.read_csv(DATA_FILE)
        excel_file = "engagement_data.xlsx"
        df.to_excel(excel_file, index=False)
        return send_file(excel_file, as_attachment=True)
    except Exception as e:
        return f"Terjadi kesalahan saat mengekspor: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)

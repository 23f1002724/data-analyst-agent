from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO

app = FastAPI()

@app.post("/api/")
async def analyze_data(files: List[UploadFile] = File(...)):
    questions_file = next((f for f in files if f.filename == "questions.txt"), None)
    if not questions_file:
        return JSONResponse(status_code=400, content={"error": "questions.txt is required"})

    questions = (await questions_file.read()).decode("utf-8")
    data_file = next((f for f in files if f.filename.endswith(".csv")), None)

    response = []

    if "How many $2 bn movies were released before 2000?" in questions:
        df = pd.read_csv(data_file.file)
        df["Worldwide gross"] = df["Worldwide gross"].replace('[\$,]', '', regex=True).astype(float)
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        count = df[(df["Worldwide gross"] >= 2_000_000_000) & (df["Year"] < 2000)].shape[0]
        response.append(count)

    if "Which is the earliest film that grossed over $1.5 bn?" in questions:
        df = pd.read_csv(data_file.file)
        df["Worldwide gross"] = df["Worldwide gross"].replace('[\$,]', '', regex=True).astype(float)
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        earliest = df[df["Worldwide gross"] > 1_500_000_000].sort_values("Year").iloc[0]["Title"]
        response.append(str(earliest))

    if "correlation between the Rank and Peak" in questions:
        df = pd.read_csv(data_file.file)
        correlation = df["Rank"].corr(df["Peak"])
        response.append(round(correlation, 6))

    if "Draw a scatterplot of Rank and Peak" in questions:
        fig, ax = plt.subplots()
        df = pd.read_csv(data_file.file)
        ax.scatter(df["Rank"], df["Peak"])
        m, b = np.polyfit(df["Rank"], df["Peak"], 1)
        ax.plot(df["Rank"], m * df["Rank"] + b, "r--")
        ax.set_xlabel("Rank")
        ax.set_ylabel("Peak")

        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)
        encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
        response.append(f"data:image/png;base64,{encoded}")

    return JSONResponse(content=response)
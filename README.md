# Data Analyst Agent

This API receives a `questions.txt` file and optional attachments (like CSVs) and answers data analysis questions using Python, Pandas, Matplotlib, and FastAPI.

## 🚀 Deployment

Deploy to [Render](https://render.com) using `render.yaml`. 

## 🧪 Testing

Use this `curl` command:

```bash
curl -X POST "https://your-render-url.onrender.com/api/" \
  -F "questions.txt=@questions.txt" \
  -F "data.csv=@data.csv"
```

## 📝 License

MIT License
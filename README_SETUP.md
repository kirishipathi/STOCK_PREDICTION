Setup and run instructions

1. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1 or activate.bat
pip install -r requirements.txt
```

2. Fetch initial stock data

```bash
python database.py
```

3. Download training data

```bash
python generate_dataset.py
```

4. Preprocess data

```bash
python preprocess.py
```

5. Train LSTM model

```bash
python train_model.py
```

6. Download intraday data

```bash
python generate_intraday_dataset.py
```

7. Prepare intraday sequences

```bash
python prepare_intraday_data.py
```

8. Train intraday models

```bash
python train_xgboost_model.py
python train_catboost_model.py
```

9. Start backend

```bash
uvicorn main:app --reload
```

10. Start frontend

```bash
cd stock-app
npm install
npm run dev
```

Notes:
- Backend runs on http://127.0.0.1:8000
- Frontend runs on http://localhost:5173
- A `.env` file may be required for `NEWS_API_KEY`.
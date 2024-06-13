import os
import joblib
from sqlalchemy import text
from app.db.session import SessionLocal


async def model_test():
    model_path = os.path.join("app", "text_classification_model.pkl")
    model = joblib.load(model_path)

    async with SessionLocal() as session:
        rows = await session.execute(text("SELECT * FROM items"))
        items = rows.fetchall()
        for row in items:
            predictions = model.predict([row.title])
            result = predictions.tolist()
            print(row.title)
            print(result)

    return True

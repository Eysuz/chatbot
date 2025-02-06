import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# OpenAI API kalitingizni shu yerga joylashtiring
openai.api_key = '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'  # API kalitini to'g'ri joylashtiring

app = FastAPI()

# CORS middleware qo'shish
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Barcha domenlarga ruxsat berish
    allow_credentials=True,
    allow_methods=["*"],  # Barcha metodlarga ruxsat berish
    allow_headers=["*"],  # Barcha sarlavhalarga ruxsat berish
)

# Foydalanuvchidan xabar olish uchun model
class Message(BaseModel):
    message: str

# Foydalanuvchi xabariga OpenAI API yordamida javob olish
def get_chat_response(user_message: str) -> str:
    try:
        # OpenAI Chat API chaqiruvi
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Tanlangan model (yoki gpt-4)
            messages=[  # Foydalanuvchi va tizimdan xabarlar
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        # Javobni qaytarish
        return response['choices'][0]['message']['content']
    except Exception as e:
        # Umumiy xatolikni qaytarish
        raise HTTPException(status_code=500, detail=f"Xato: {str(e)}")

@app.post("/chat")
async def chat(message: Message):
    # Foydalanuvchidan xabarni olish
    user_message = message.message
    
    # AI javobini olish
    ai_response = get_chat_response(user_message)
    
    # AI javobini foydalanuvchiga qaytarish
    return {"response": ai_response}

# FastAPI serverni ishga tushirish
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

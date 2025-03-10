from flask import Flask, request, jsonify
import requests
from openai import OpenAI

app = Flask(__name__)

# API Keys (Replace with your actual keys)
NEWS_API_KEY = "ff03801c758443ac93708c70ebbebad5"
WEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
OPENROUTER_API_KEY = "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"

# Initialize OpenRouter client
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)

chat_history = [{"role": "system", "content": "You are a helpful AI assistant."}]

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        description = response["weather"][0]["description"]
        return f"The weather in {city} is {temp}°C with {description}."
    return "⚠️ Unable to fetch weather data."

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    if response.get("articles"):
        headlines = [article["title"] for article in response["articles"][:3]]
        return "\n".join(headlines)
    return "⚠️ Unable to fetch news."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    
    if user_input.lower().startswith("weather "):
        city = user_input.split(" ", 1)[1]
        return jsonify({"response": get_weather(city)})
    elif user_input.lower() == "news":
        return jsonify({"response": get_news()})
    
    chat_history.append({"role": "user", "content": user_input})
    
    completion = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=chat_history
    )
    
    if completion and completion.choices:
        ai_response = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": ai_response})
        return jsonify({"response": ai_response})

    return jsonify({"response": "⚠️ AI did not return a valid response."})
@app.route("/")
def home():
    return "🤖 AI Chatbot API is running! Use POST /chat to interact."


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
import requests
from openai import OpenAI

app = Flask(__name__)

# API Keys (Replace with your actual keys)
NEWS_API_KEY = "ff03801c758443ac93708c70ebbebad5"
WEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
OPENROUTER_API_KEY = "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"

# Initialize OpenRouter client
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)

chat_history = [{"role": "system", "content": "You are a helpful AI assistant."}]

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        description = response["weather"][0]["description"]
        return f"The weather in {city} is {temp}°C with {description}."
    return "⚠️ Unable to fetch weather data."

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    if response.get("articles"):
        headlines = [article["title"] for article in response["articles"][:3]]
        return "\n".join(headlines)
    return "⚠️ Unable to fetch news."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    
    if user_input.lower().startswith("weather "):
        city = user_input.split(" ", 1)[1]
        return jsonify({"response": get_weather(city)})
    elif user_input.lower() == "news":
        return jsonify({"response": get_news()})
    
    chat_history.append({"role": "user", "content": user_input})
    
    completion = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=chat_history
    )
    
    if completion and completion.choices:
        ai_response = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": ai_response})
        return jsonify({"response": ai_response})

    return jsonify({"response": "⚠️ AI did not return a valid response."})

if __name__ == "__main__":
    app.run(debug=True)

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API key is missing. Set the OPENAI_API_KEY environment variable.")

exposition = ("You serve as a basketball coach providing specific advice on how a player's "
              "mechanics can improve based on quantitative differences between their form and textbook form. "
              "Use the context provided about biomechanics in addition to the user's personal metrics in "
              "order to suggest appropriate changes.")

conversation_history = [
    {"role": "system", "content": exposition}
]

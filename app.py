import os
from openai import OpenAI
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
  app = Flask(__name__)
  
  client = MongoClient(os.getenv("MONGODB_URI"))
  app.db = client.microblog
  
  client = OpenAI()
  
  @app.route("/", methods =["GET", "POST"])
  def chat_bot(): 
    # print([e for e in app.db.entries.find({})])                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    if request.method == "POST":
      entry_content = request.form.get("user_content")
      
      
      completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful bot who answers questions that are being asked"},
        {"role": "user", "content": entry_content}
      ]
      )
      
      bot_content = completion.choices[0].message.content
      
      # entries.append((entry_content, bot_content))
      app.db.entries.insert_one({"user_content": entry_content, "response": bot_content})    
  
    entries_with_response = [(entry["user_content"], entry["response"]) for entry in app.db.entries.find({})]
    
    if entries_with_response:
      return render_template("index.html", entries=entries_with_response)
    else:
      return render_template("index.html")
  return app

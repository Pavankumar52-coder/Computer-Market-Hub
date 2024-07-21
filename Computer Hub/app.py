import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

with open('corpus.json', 'r') as f:
    corpus = json.load(f)

# Store the conversation history
conversation_history = []

def find_answer(user_message):
    global conversation_history
    
    # Combine the user message with the previous conversation history
    context = ' '.join(conversation_history) + ' ' + user_message
    
    # Search for the answer in the corpus
    for qa in corpus:
        if qa['question'].lower() in context.lower():
            return qa['answer']
    
    return "For further assistance, please contact us directly."

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    # Append user message to the conversation history
    conversation_history.append(user_message)
    
    response = find_answer(user_message)
    
    # Append bot response to the conversation history
    conversation_history.append(response)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
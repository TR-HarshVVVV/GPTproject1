from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ChatDatabase:
    def __init__(self):
        # Get MongoDB connection string from environment variable
        mongo_uri = os.getenv('MONGODB_URI', 'mongodb+srv://your-connection-string')
        self.client = MongoClient(mongo_uri)
        self.db = self.client['ollama_chat']
        self.chats = self.db['chats']
        self.messages = self.db['messages']
        
        # Create indexes
        self.chats.create_index('updated_at')
        self.messages.create_index([('chat_id', 1), ('timestamp', 1)])

    def create_chat(self, title, model):
        chat = {
            'title': title,
            'model': model,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        result = self.chats.insert_one(chat)
        return str(result.inserted_id)

    def add_message(self, chat_id, role, content):
        message = {
            'chat_id': chat_id,
            'role': role,
            'content': content,
            'timestamp': datetime.now()
        }
        result = self.messages.insert_one(message)
        
        # Update chat's updated_at
        self.chats.update_one(
            {'_id': chat_id},
            {'$set': {'updated_at': datetime.now()}}
        )
        return str(result.inserted_id)

    def get_chat(self, chat_id):
        chat = self.chats.find_one({'_id': chat_id})
        if chat:
            messages = list(self.messages.find(
                {'chat_id': chat_id}
            ).sort('timestamp', 1))
            
            return {
                'id': str(chat['_id']),
                'title': chat['title'],
                'model': chat['model'],
                'created_at': chat['created_at'].isoformat(),
                'updated_at': chat['updated_at'].isoformat(),
                'messages': [
                    {
                        'id': str(msg['_id']),
                        'role': msg['role'],
                        'content': msg['content'],
                        'timestamp': msg['timestamp'].isoformat()
                    } for msg in messages
                ]
            }
        return None

    def get_all_chats(self):
        chats = list(self.chats.find().sort('updated_at', -1))
        return [
            {
                'id': str(chat['_id']),
                'title': chat['title'],
                'model': chat['model'],
                'created_at': chat['created_at'].isoformat(),
                'updated_at': chat['updated_at'].isoformat()
            } for chat in chats
        ]

    def delete_chat(self, chat_id):
        # Delete all messages first
        self.messages.delete_many({'chat_id': chat_id})
        # Then delete the chat
        self.chats.delete_one({'_id': chat_id}) 
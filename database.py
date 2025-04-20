from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables
load_dotenv()

class ChatDatabase:
    def __init__(self):
        # Get MongoDB connection string from environment variable
        mongo_uri = os.getenv('MONGODB_URI')
        if not mongo_uri:
            raise ValueError("MONGODB_URI environment variable is not set")
            
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
        try:
            # Convert string ID to ObjectId
            chat_id_obj = ObjectId(chat_id)
            
            message = {
                'chat_id': chat_id_obj,
                'role': role,
                'content': content,
                'timestamp': datetime.now()
            }
            result = self.messages.insert_one(message)
            
            # Update chat's updated_at
            self.chats.update_one(
                {'_id': chat_id_obj},
                {'$set': {'updated_at': datetime.now()}}
            )
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error adding message: {str(e)}")
            raise

    def get_chat(self, chat_id):
        try:
            # Convert string ID to ObjectId
            chat_id_obj = ObjectId(chat_id)
            
            chat = self.chats.find_one({'_id': chat_id_obj})
            if chat:
                messages = list(self.messages.find(
                    {'chat_id': chat_id_obj}
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
        except Exception as e:
            print(f"Error getting chat: {str(e)}")
            raise

    def get_all_chats(self):
        try:
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
        except Exception as e:
            print(f"Error getting all chats: {str(e)}")
            raise

    def delete_chat(self, chat_id):
        try:
            # Convert string ID to ObjectId
            chat_id_obj = ObjectId(chat_id)
            
            # Delete all messages first
            self.messages.delete_many({'chat_id': chat_id_obj})
            # Then delete the chat
            self.chats.delete_one({'_id': chat_id_obj})
        except Exception as e:
            print(f"Error deleting chat: {str(e)}")
            raise 
# Setting Up MongoDB Atlas

Follow these steps to set up a MongoDB Atlas database for your Ollama Chat Web application:

## 1. Create a MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for a free account
3. Choose the free tier (M0) when prompted

## 2. Create a Cluster

1. Click "Build a Database"
2. Select "FREE" tier
3. Choose a cloud provider (AWS, Google Cloud, or Azure) and a region close to you
4. Click "Create Cluster"

## 3. Set Up Database Access

1. In the left sidebar, click "Database Access"
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Enter a username and password (make sure to remember these)
5. Set privileges to "Read and write to any database"
6. Click "Add User"

## 4. Set Up Network Access

1. In the left sidebar, click "Network Access"
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (for development) or add your specific IP
4. Click "Confirm"

## 5. Get Your Connection String

1. In the left sidebar, click "Database"
2. Click "Connect"
3. Select "Connect your application"
4. Copy the connection string
5. Replace `<password>` with your database user password
6. Replace `<dbname>` with `ollama_chat`

## 6. Add the Connection String to Your .env File

Create a `.env` file in your project root with the following content:

```
MONGODB_URI=your_connection_string_here
```

Replace `your_connection_string_here` with the connection string you copied in step 5.

## 7. Test Your Connection

Run your application and check if it can connect to MongoDB Atlas. If everything is set up correctly, you should be able to create and retrieve chats from the database.

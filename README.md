# Sentiment-Aware-Customer-Support-Chatbot-AWS-
This project is a customer support chatbot with sentiment analysis built using AWS services. 
It helps organizations provide automated customer support, track sentiment in real-time, and store feedback for future analysis.

## 🎥 Demo Video:-
The above two videos demonstrates the full functionality and working of the sentiment-aware chatbot, 
including AWS Lex integration, Lambda-based logic, real-time sentiment analysis with Amazon Comprehend, and conversation storage in DynamoDB.

---

## 🛠️ Features
- **Chatbot with Amazon Lex** for customer support.
- **AWS Lambda** to process responses and integrate with backend logic.
- **Amazon Comprehend** for real-time sentiment analysis.
- **Amazon DynamoDB** to store conversation data and feedback.
- **Kommunicate Integration** to embed chatbot on a website.

---

## 🏗️ Architecture
![Architecture Diagram](docs/architecture.png)

**Architecture Overview:**
1. User interacts with the chatbot on a website (Kommunicate).
2. Amazon Lex manages the conversation flow.
3. AWS Lambda processes logic and queries sentiment from Amazon Comprehend.
4. DynamoDB stores user messages, feedback, and sentiment.
5. Admins can analyze conversation sentiment trends for better support.

---

## 🔧 AWS Services Used
| Service               | Purpose                                  |
|----------------------|------------------------------------------|
| **Amazon Lex**        | Natural language chatbot interface       |
| **AWS Lambda**        | Serverless backend logic                 |
| **Amazon Comprehend** | Sentiment analysis of user messages      |
| **Amazon DynamoDB**   | Conversation and feedback storage        |
| **Kommunicate**       | Website integration for chatbot          |

---

## 🚀 How It Works
1. User sends a message via chatbot widget.
2. Lambda processes the input, triggers sentiment analysis.
3. Sentiment score is recorded in DynamoDB.
4. The chatbot responds accordingly and adapts based on sentiment.

---

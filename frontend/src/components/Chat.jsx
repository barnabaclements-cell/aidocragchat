import { useState } from "react";
import axios from "axios";

function Chat() {

    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);

    const askQuestion = async () => {

        if (!question) return;

        const userMessage = {
            sender: "You",
            text: question,
        };

        setMessages((prev) => [...prev, userMessage]);

        try {

            const res = await axios.post(
                "http://127.0.0.1:8000/api/chat/",
                {
                    question,
                }
            );

            const botMessage = {
                sender: "AI",
                text: res.data.answer,
            };

            setMessages((prev) => [...prev, botMessage]);

        } catch (err) {

            const botMessage = {
                sender: "AI",
                text: "Error contacting server.",
            };

            setMessages((prev) => [...prev, botMessage]);

        }

        setQuestion("");

    };

    return (

        <div className="card">

            <h2>Chat</h2>

            <div className="chat-box">

                {
                    messages.map((msg, index) => (

                        <div key={index} className="message">

                            <strong>{msg.sender}:</strong>

                            <p>{msg.text}</p>

                        </div>

                    ))
                }

            </div>

            <input
                type="text"
                placeholder="Ask about the document..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
            />

            <button onClick={askQuestion}>
                Send
            </button>

        </div>

    );
}

export default Chat;
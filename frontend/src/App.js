// frontend/src/components/Chat.jsx
import { useState } from "react";
import axios from "axios";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = {
      sender: "user",
      text: input,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    try {
      const response = await axios.post("http://localhost:8080/get", { msg: input });
      const botMsg = {
        sender: "bot",
        text: response.data,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-blue-50 to-blue-100">
      <div className="w-full max-w-lg bg-white shadow-xl rounded-2xl flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center gap-3 bg-blue-600 text-white p-4">
          <img
            src="https://cdn-icons-png.flaticon.com/512/387/387569.png"
            alt="bot"
            className="w-10 h-10 rounded-full border-2 border-white"
          />
          <div>
            <h2 className="text-lg font-semibold">Medical Chatbot</h2>
            <p className="text-sm">Ask me anything!</p>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
            >
              {msg.sender === "bot" && (
                <img
                  src="https://cdn-icons-png.flaticon.com/512/387/387569.png"
                  alt="bot"
                  className="w-8 h-8 rounded-full mr-2"
                />
              )}
              <div
                className={`px-4 py-2 rounded-2xl max-w-xs ${
                  msg.sender === "user"
                    ? "bg-blue-500 text-white rounded-br-none"
                    : "bg-gray-200 text-gray-900 rounded-bl-none"
                }`}
              >
                <p>{msg.text}</p>
                <span className="text-xs text-gray-500 block text-right">{msg.time}</span>
              </div>
              {msg.sender === "user" && (
                <img
                  src="https://i.ibb.co/d5b84Xw/Untitled-design.png"
                  alt="user"
                  className="w-8 h-8 rounded-full ml-2"
                />
              )}
            </div>
          ))}
        </div>

        {/* Input */}
        <form onSubmit={sendMessage} className="flex items-center border-t p-3">
          <input
            type="text"
            className="flex-1 border rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button
            type="submit"
            className="ml-2 p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-full"
          >
            <i className="fas fa-location-arrow"></i>
          </button>
        </form>
      </div>
    </div>
  );
}

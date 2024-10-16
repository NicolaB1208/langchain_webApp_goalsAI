import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [messages, setMessages] = useState([{ sender: 'bot', text: 'Hey there! I will help you with your goals. Ready to start?' }]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const messagesEndRef = useRef(null);
  const inputAreaRef = useRef(null); // Ref for the textarea

  const adjustTextareaHeight = () => {
    if (inputAreaRef.current) {
      inputAreaRef.current.style.height = 'inherit'; // Reset height to recalibrate
      inputAreaRef.current.style.height = `${inputAreaRef.current.scrollHeight}px`; // Set new height
    }
  };
  
  const formatMessage = (text) => {
    const boldRegex = /\*\*(.*?)\*\*/g;
    return text.split('\n').map((line, index) => {
      const lineWithBold = line.replace(boldRegex, (match, p1) => `<strong>${p1}</strong>`);

      if (line.match(/^\d\./)) {
        return <li key={index} dangerouslySetInnerHTML={{ __html: lineWithBold }} />;
      } else if (line.trim() === '') {
        return <br key={index} />;
      } else {
        return <p key={index} dangerouslySetInnerHTML={{ __html: lineWithBold }} />;
      }
    });
  
    return <>{formattedLines}</>;
  };
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async () => {
    if (input.trim() === '') return;

    setIsThinking(true); // Start thinking animation
    const newMessages = [...messages, { sender: 'user', text: input }];
    setMessages(newMessages);
    setInput('');

    try {
      const response = await axios.post('/ask', { transcript: newMessages }, { withCredentials: true });
      const botMessage = response.data;
      setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: botMessage }]);
    } catch (error) {
      console.error('Error sending message:', error);
    }  finally {
      setIsThinking(false); // Stop thinking animation
    }
  };

  useEffect(() => {
    adjustTextareaHeight(); // Adjust height on component mount and input change
  }, [input]);

  useEffect(() => {
    if (inputAreaRef.current) {
      inputAreaRef.current.focus(); // Auto-focus on mount
    }
  }, []); // The empty array causes this effect to only run on mount
  
  return (
    <div className="chatbot">
      <div className="messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            <div className="message-title">{message.sender === 'user' ? 'You' : 'GoalsAI Coach'}</div>
            <div>{formatMessage(message.text)}</div>
          </div>
        ))}
        {isThinking && <div className="thinking-animation"></div>} {/* This line will always show the animation */}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="input-area">
        <textarea
          ref={inputAreaRef} // Attach the ref to the textarea
          value={input}
          onChange={(e) => {
            setInput(e.target.value);
            adjustTextareaHeight(); // Adjust height every time the content changes
          }}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              sendMessage();
            }
          }}
          placeholder="You can do it..."
          rows={1}
        ></textarea>
        <button onClick={sendMessage} className="send-button" aria-label="Send message">
          <img src="/sun_icon.svg" alt="Send Message" />
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
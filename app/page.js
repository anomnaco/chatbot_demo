"use client";
import { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import update from 'immutability-helper';
import Bubble from '@/components/Bubble'

export default function Home() {
  const [messages, setMessages] = useState([]);

  const inputRef = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();

    if (inputRef.current.value.trim() !== "") {
      try {
        const question = inputRef.current.value;
        setMessages(prev => [...prev, { text: question, isQuestion: true }]);
        inputRef.current.value = "";
        inputRef.current.focus();
        setMessages(prev => [...prev, { processing: true }]);
        const res = await axios.post(`${NEXT_PUBLIC_API_URL}/api/chat`, {
          prompt: question,
        });
        const reply = JSON.parse(res.data);
        setMessages(prev => {
          const p = update(prev, { [prev.length - 1]: { text: { $set: reply.text }, url: { $set: reply.url }, processing: { $set: false } } });
          console.log(res.data, prev, p);
          return p;
        });
      } catch (err) {

      }
    }
  }

  return (
    <main className="flex h-screen flex-col items-center justify-center">
      <section className='chatbot-section flex flex-col origin:w-[800px] w-full origin:h-[600px] h-full rounded-md p-2 md:p-6'>
        <h1 className='chatbot-text-primary text-xl md:text-2xl font-medium'>Chatbot App</h1>
        <div className='flex-1 relative overflow-y-auto my-4 md:my-6'>
          <div className='absolute w-full'>
            {messages.map((message, index) => <Bubble ref={messagesEndRef} key={`message-${index}`} content={message} />)}
          </div>
        </div>
        <form className='flex h-[40px] gap-2' onSubmit={sendMessage}>
          <input ref={inputRef} className='chatbot-input flex-1 text-sm md:text-base outline-none bg-transparent rounded-md p-2' placeholder='Send a message...' />
          <button type="submit" className='chatbot-send-button flex rounded-md items-center justify-center px-2.5 origin:px-3'>
            <svg width="20" height="20" viewBox="0 0 20 20">
              <path d="M2.925 5.025L9.18333 7.70833L2.91667 6.875L2.925 5.025ZM9.175 12.2917L2.91667 14.975V13.125L9.175 12.2917ZM1.25833 2.5L1.25 8.33333L13.75 10L1.25 11.6667L1.25833 17.5L18.75 10L1.25833 2.5Z" />
            </svg>
            <span className='hidden origin:block font-semibold text-sm ml-2'>Send</span>
          </button>
        </form>
      </section>
    </main>
  )
}

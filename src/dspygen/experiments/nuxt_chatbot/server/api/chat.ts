import { defineEventHandler, readBody } from 'h3';
import Groq from 'groq-sdk';

const openaiApiKey = process.env.OPiAI_API_KEY; // not to load from OS ENV
const groqApiKey = process.env.GROQ_API_KEY;

const groq = new Groq({
  apiKey: groqApiKey
});

const fetchOpenAIResponse = async (message, model, apiKey) => {
  const API_URL = 'https://api.openai.com/v1/chat/completions';

  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: model,
      messages: [{ role: 'user', content: message }],
      max_tokens: 300
    })
  };

  try {
    const response = await fetch(API_URL, requestOptions);
    const data = await response.json();
    if (data.choices) return { text: data.choices[0].message.content.trim() };
    return {text: 'No Key Provided - Enter Coins'};
  } catch (error) {
    console.error('Error fetching OpenAI response:', error);
    throw new Error('Failed to fetch OpenAI response');
  }
};

const fetchGroqResponse = async (message, model) => {
  try {
    const chatCompletion = await groq.chat.completions.create({
      messages: [
        {
          role: "user",
          content: message
        }
      ],
      model: model,
      max_tokens: 500
    });

    return { text: chatCompletion.choices[0]?.message?.content || "" };
  } catch (error) {
    console.error('Error fetching Groq Cloud response:', error);
    throw new Error('Failed to fetch Groq Cloud response');
  }
};

export default defineEventHandler(async (event) => {
  const { message, service, model } = await readBody(event);

  try {
    if (service === 'openai' && openaiApiKey) {
      return await fetchOpenAIResponse(message, model, openaiApiKey);
    } else if (service === 'groq' ) {
      return await fetchGroqResponse(message, model);
    } else {
      throw new Error('Invalid service selected');
    }
  } catch (error) {
    console.error('Error in API handler:', error);
    return {text: 'No Paid Key Provided - Enter Coins'};
  }
});

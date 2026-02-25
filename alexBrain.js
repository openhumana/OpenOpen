const Groq = require("groq-sdk");

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

async function askAlex(userInput) {
  try {
    const chatCompletion = await groq.chat.completions.create({
      messages: [
        {
          role: "system",
          content: "You are Alex, the Lead Digital Associate for Open Humana. You are professional, tech-savvy, and efficient. You help the owner manage agency tasks and coding projects. Keep your answers concise."
        },
        {
          role: "user",
          content: userInput,
        },
      ],
      model: "llama-3.3-70b-versatile",
    });

    return chatCompletion.choices[0].message.content;
  } catch (error) {
    console.error("Groq Brain Error:", error);
    return "Sorry, I'm having a bit of a headache. Can you try again?";
  }
}

module.exports = { askAlex };
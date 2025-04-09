const venom = require('venom-bot');
const fetch = require('node-fetch');
require('dotenv').config();

const MEU_NUMERO = process.env.MEU_NUMERO; // formato: 55xxxxxxxxxxx@c.us

venom
  .create({
    session: 'whatsapp-bot'
  })
  .then((client) => start(client))
  .catch((error) => console.log(error));

function start(client) {
  client.onMessage(async (message) => {
    // Ignorar mensagens que não são suas
    if (message.from !== MEU_NUMERO || message.isGroupMsg) return;

    const userInput = message.body;

    // Chamada à API da OpenAI
    const gptResponse = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'gpt-4-1106-preview',
        messages: [
          {
            role: 'system',
            content: 'Você é um assistente financeiro. Receba mensagens como "mercado 72,50", e responda com uma função registrar_gasto com descrição, valor, categoria e data.'
          },
          {
            role: 'user',
            content: userInput
          }
        ],
        functions: [
          {
            name: 'registrar_gasto',
            description: 'Registra um gasto no Supabase',
            parameters: {
              type: 'object',
              properties: {
                descricao: { type: 'string' },
                valor: { type: 'number' },
                categoria: { type: 'string' },
                data: { type: 'string', format: 'date-time' }
              },
              required: ['descricao', 'valor', 'categoria', 'data']
            }
          }
        ],
        function_call: 'auto'
      })
    });

    const gptJson = await gptResponse.json();
    const call = gptJson.choices?.[0]?.message?.function_call;
    if (!call || call.name !== 'registrar_gasto') return;

    const args = JSON.parse(call.arguments);

    // Chamada à Supabase Edge Function
    const supabaseResponse = await fetch(process.env.SUPABASE_FUNCTION_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.SUPABASE_SERVICE_KEY}`
      },
      body: JSON.stringify({
        ...args,
        origem: 'whatsapp'
      })
    });

    const result = await supabaseResponse.json();

    if (result && !result.error) {
      await client.sendText(message.from, `✅ Gasto registrado: ${args.descricao} - R$${args.valor}`);
    } else {
      await client.sendText(message.from, `❌ Erro ao registrar gasto: ${result.error || 'desconhecido'}`);
    }
  });
}
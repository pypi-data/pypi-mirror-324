import {
  type Message,
  createDataStreamResponse,
  smoothStream,
  streamText,
} from 'ai';

import { auth } from '@/app/(auth)/auth';
import { customModel } from '@/lib/ai';
import { models } from '@/lib/ai/models';
import { systemPrompt } from '@/lib/ai/prompts';
import {
  deleteChatById,
  getChatById,
  saveChat,
  saveMessages,
} from '@/lib/db/queries';
import {
  generateUUID,
  getMostRecentUserMessage,
  sanitizeResponseMessages,
} from '@/lib/utils';

import { generateTitleFromUserMessage } from '../../actions';
import { createDocument } from '@/lib/ai/tools/create-document';
import { updateDocument } from '@/lib/ai/tools/update-document';
import { requestSuggestions } from '@/lib/ai/tools/request-suggestions';
import { getWeather } from '@/lib/ai/tools/get-weather';

const FASTAPI_URL = 'http://localhost:8000';

async function fetchChainOfThought(messages: Message[]) {
  try {
    const response = await fetch(`${FASTAPI_URL}/api/chat/chain`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: messages.map(msg => ({
          role: msg.role,
          content: msg.content
        }))
      }),
    });

    if (!response.ok) {
      throw new Error(`FastAPI error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Chain of thought error:', error);
    return null;
  }
}

export const maxDuration = 60;

type AllowedTools =
  | 'createDocument'
  | 'updateDocument'
  | 'requestSuggestions'
  | 'getWeather';

const blocksTools: AllowedTools[] = [
  'createDocument',
  'updateDocument',
  'requestSuggestions',
];

const weatherTools: AllowedTools[] = ['getWeather'];
const allTools: AllowedTools[] = [...blocksTools, ...weatherTools];

export async function POST(request: Request) {
  const {
    id,
    messages,
    modelId,
  }: { id: string; messages: Array<Message>; modelId: string } =
    await request.json();

  const session = await auth();

  if (!session || !session.user || !session.user.id) {
    return new Response('Unauthorized', { status: 401 });
  }

  const model = models.find((model) => model.id === modelId);

  if (!model) {
    return new Response('Model not found', { status: 404 });
  }

  const userMessage = getMostRecentUserMessage(messages);

  if (!userMessage) {
    return new Response('No user message found', { status: 400 });
  }

  const chat = await getChatById({ id });

  if (!chat) {
    const title = await generateTitleFromUserMessage({ message: userMessage });
    await saveChat({ id, userId: session.user.id, title });
  }

  await saveMessages({
    messages: [{ ...userMessage, createdAt: new Date(), chatId: id }],
  });

  // Get chain of thought from FastAPI
  let chainOfThoughtMetadata = {};
  try {
    const chainResponse = await fetchChainOfThought(messages);
    if (chainResponse) {
      chainOfThoughtMetadata = {
        chainOfThought: chainResponse.chainOfThought,
        initialSolution: chainResponse.initialSolution
      };
      
      // Use the refined solution for the model
      messages = messages.map(msg => 
        msg.id === userMessage.id 
          ? { 
              ...msg, 
              content: chainResponse.finalSolution,
              metadata: chainOfThoughtMetadata 
            }
          : msg
      );
    }
  } catch (error) {
    console.error('FastAPI chain of thought error:', error);
    // Continue without chain of thought if FastAPI call fails
  }

  return createDataStreamResponse({
    execute: (dataStream) => {
      const result = streamText({
        model: customModel(model.apiIdentifier),
        system: systemPrompt,
        messages,
        maxSteps: 5,
        experimental_activeTools: allTools,
        experimental_transform: smoothStream({ chunking: 'word' }),
        experimental_generateMessageId: generateUUID,
        tools: {
          getWeather,
          createDocument: createDocument({ session, dataStream, model }),
          updateDocument: updateDocument({ session, dataStream, model }),
          requestSuggestions: requestSuggestions({
            session,
            dataStream,
            model,
          }),
        },
        onFinish: async ({ response }) => {
          if (session.user?.id) {
            try {
              const responseMessagesWithoutIncompleteToolCalls =
                sanitizeResponseMessages(response.messages);

              // Add chain of thought metadata to assistant messages
              const enhancedMessages = responseMessagesWithoutIncompleteToolCalls.map(
                (message) => ({
                  id: message.id,
                  chatId: id,
                  role: message.role,
                  content: message.content,
                  createdAt: new Date(),
                  metadata: message.role === 'assistant' ? chainOfThoughtMetadata : undefined
                })
              );

              await saveMessages({
                messages: enhancedMessages,
              });
            } catch (error) {
              console.error('Failed to save chat');
            }
          }
        },
        experimental_telemetry: {
          isEnabled: true,
          functionId: 'stream-text',
        },
      });

      result.mergeIntoDataStream(dataStream);
    },
  });
}

export async function DELETE(request: Request) {
  const { searchParams } = new URL(request.url);
  const id = searchParams.get('id');

  if (!id) {
    return new Response('Not Found', { status: 404 });
  }

  const session = await auth();

  if (!session || !session.user) {
    return new Response('Unauthorized', { status: 401 });
  }

  try {
    const chat = await getChatById({ id });

    if (chat.userId !== session.user.id) {
      return new Response('Unauthorized', { status: 401 });
    }

    await deleteChatById({ id });

    return new Response('Chat deleted', { status: 200 });
  } catch (error) {
    return new Response('An error occurred while processing your request', {
      status: 500,
    });
  }
}
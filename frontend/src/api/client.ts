import { QuestionResponse } from '../types';

// Stub API client for development - no actual network calls
export const bookApi = {
  askQuestion: async (question: string): Promise<QuestionResponse> => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Return a stub response
    const stubAnswer = `This is a stub response to your question: "${question}". 

In the real implementation, this would send your question along with the full text of "The Way of Kings" to OpenAI for an AI-generated answer.

For now, this is just a placeholder to test the frontend functionality. The backend integration will be implemented later.`;
    
    return {
      answer: stubAnswer
    };
  },
};

export default bookApi; 
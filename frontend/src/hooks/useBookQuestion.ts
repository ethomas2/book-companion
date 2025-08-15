import { useMutation } from '@tanstack/react-query';
import { bookApi } from '../api/client';

export const useBookQuestion = () => {
  return useMutation({
    mutationFn: bookApi.askQuestion,
    onSuccess: (data, variables) => {
      // You could add success handling here (e.g., add to question history)
      console.log('Question answered successfully:', { question: variables, answer: data.answer });
    },
    onError: (error) => {
      console.error('Failed to get answer:', error);
    },
  });
}; 
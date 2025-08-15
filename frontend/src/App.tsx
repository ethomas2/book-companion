import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import BookQuestionForm from './components/BookQuestionForm';
import './App.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="App">
        <BookQuestionForm />
      </div>
    </QueryClientProvider>
  );
}

export default App;

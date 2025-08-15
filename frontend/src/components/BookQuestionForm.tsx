import React, { useState } from 'react';
import { useBookQuestion } from '../hooks/useBookQuestion';

const BookQuestionForm: React.FC = () => {
  const [question, setQuestion] = useState('');
  const { mutate: askQuestion, isPending, error, data } = useBookQuestion();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (question.trim()) {
      askQuestion(question);
    }
  };

  const handleTestQuestion = () => {
    askQuestion('Who is Kaladin?');
  };

  const containerStyle: React.CSSProperties = {
    maxWidth: '64rem',
    margin: '0 auto',
    padding: '1.5rem',
  };

  const titleStyle: React.CSSProperties = {
    fontSize: '1.875rem',
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: '2rem',
    color: '#1f2937',
  };

  const formStyle: React.CSSProperties = {
    marginBottom: '2rem',
  };

  const labelStyle: React.CSSProperties = {
    fontSize: '1.125rem',
    fontWeight: '500',
    color: '#374151',
    marginBottom: '0.5rem',
  };

  const textareaStyle: React.CSSProperties = {
    width: '100%',
    padding: '1rem',
    border: '1px solid #d1d5db',
    resize: 'none',
    fontSize: '1rem',
    fontFamily: 'inherit',
  };

  const buttonStyle: React.CSSProperties = {
    padding: '0.75rem 1.5rem',
    backgroundColor: '#2563eb',
    color: 'white',
    fontWeight: '500',
    borderRadius: '0.5rem',
    border: 'none',
    cursor: 'pointer',
    fontSize: '1rem',
  };

  const buttonDisabledStyle: React.CSSProperties = {
    ...buttonStyle,
    backgroundColor: '#9ca3af',
    cursor: 'not-allowed',
  };

  const testButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    backgroundColor: '#059669',
    marginLeft: '1rem',
  };

  const errorStyle: React.CSSProperties = {
    marginBottom: '1.5rem',
    padding: '1rem',
    backgroundColor: '#fef2f2',
    border: '1px solid #f87171',
    color: '#dc2626',
    borderRadius: '0.5rem',
  };

  const answerStyle: React.CSSProperties = {
    backgroundColor: '#f9fafb',
    padding: '1.5rem',
    borderRadius: '0.5rem',
    border: '1px solid #e5e7eb',
  };

  const answerTitleStyle: React.CSSProperties = {
    fontSize: '1.25rem',
    fontWeight: '600',
    marginBottom: '1rem',
    color: '#1f2937',
  };

  const answerTextStyle: React.CSSProperties = {
    color: '#374151',
    lineHeight: '1.6',
    whiteSpace: 'pre-wrap',
  };

  const loadingStyle: React.CSSProperties = {
    textAlign: 'center',
    padding: '2rem',
  };

  const spinnerStyle: React.CSSProperties = {
    display: 'inline-block',
    width: '2rem',
    height: '2rem',
    border: '2px solid #e5e7eb',
    borderTop: '2px solid #2563eb',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  };

  const loadingTextStyle: React.CSSProperties = {
    marginTop: '0.5rem',
    color: '#6b7280',
  };

  return (
    <div style={containerStyle}>
      <h1 style={titleStyle}>
        Ask About "The Way of Kings"
      </h1>
      
      <form onSubmit={handleSubmit} style={formStyle}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <label htmlFor="question" style={labelStyle}>
            What would you like to know about the book?
          </label>
          <textarea
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., What happened to Kaladin in chapter 5? Who is Szeth? What are Shardblades?"
            style={textareaStyle}
            rows={4}
            disabled={isPending}
          />
          <div style={{ display: 'flex', gap: '1rem' }}>
            <button
              type="submit"
              disabled={isPending || !question.trim()}
              style={isPending || !question.trim() ? buttonDisabledStyle : buttonStyle}
            >
              {isPending ? 'Asking...' : 'Ask Question'}
            </button>
            <button
              type="button"
              onClick={handleTestQuestion}
              disabled={isPending}
              style={isPending ? buttonDisabledStyle : testButtonStyle}
            >
              Test with Sample Question
            </button>
          </div>
        </div>
      </form>

      {error && (
        <div style={errorStyle}>
          <strong>Error:</strong> {error.message}
        </div>
      )}

      {data && (
        <div style={answerStyle}>
          <h2 style={answerTitleStyle}>Answer:</h2>
          <div>
            <p style={answerTextStyle}>
              {data.answer}
            </p>
          </div>
        </div>
      )}

      {isPending && (
        <div style={loadingStyle}>
          <div style={spinnerStyle}></div>
          <p style={loadingTextStyle}>Thinking about your question...</p>
        </div>
      )}
    </div>
  );
};

export default BookQuestionForm; 
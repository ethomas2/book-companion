export interface BookQuestion {
  id: string;
  question: string;
  answer: string;
  timestamp: Date;
}

export interface QuestionRequest {
  question: string;
}

export interface QuestionResponse {
  answer: string;
}

export interface ApiError {
  message: string;
  status?: number;
} 
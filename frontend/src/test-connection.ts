// Simple test to verify backend connection
import { bookApi } from './api/client';

export const testBackendConnection = async () => {
  try {
    console.log('Testing backend connection...');
    const response = await bookApi.askQuestion('Who is Kaladin?');
    console.log('✅ Backend connection successful:', response);
    return true;
  } catch (error) {
    console.error('❌ Backend connection failed:', error);
    return false;
  }
}; 
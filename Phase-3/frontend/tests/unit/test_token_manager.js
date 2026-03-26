// frontend/tests/unit/test_token_manager.js

// Mock localStorage
const mockLocalStorage = (() => {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key]),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString();
    }),
    removeItem: jest.fn((key) => {
      delete store[key];
    }),
    clear: jest.fn(() => {
      store = {};
    })
  };
})();

// Mock window.localStorage
Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage
});

import TokenManager from '../../src/lib/token_manager';

describe('TokenManager', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
    // Clear localStorage
    mockLocalStorage.clear();
  });

  describe('setToken and getToken', () => {
    test('should store and retrieve token correctly', () => {
      const token = 'test.jwt.token';
      
      TokenManager.setToken(token);
      
      expect(mockLocalStorage.setItem).toHaveBeenCalledWith('auth_token', token);
      
      const retrievedToken = TokenManager.getToken();
      expect(retrievedToken).toBe(token);
    });
  });

  describe('removeToken', () => {
    test('should remove token from storage', () => {
      TokenManager.setToken('test.jwt.token');
      TokenManager.removeToken();
      
      expect(mockLocalStorage.removeItem).toHaveBeenCalledWith('auth_token');
    });
  });

  describe('decodeToken', () => {
    test('should decode a valid JWT token', () => {
      // A simple JWT with payload: { user_id: "test_user", email: "test@example.com", exp: 9999999999 }
      const token = 'header.' + btoa(JSON.stringify({ 
        user_id: 'test_user', 
        email: 'test@example.com', 
        exp: 9999999999 
      })) + '.signature';
      
      const payload = TokenManager.decodeToken(token);
      
      expect(payload).toEqual({
        user_id: 'test_user',
        email: 'test@example.com',
        exp: 9999999999
      });
    });

    test('should return null for invalid token format', () => {
      const invalidToken = 'invalid.token.format.with.four.parts';
      
      const payload = TokenManager.decodeToken(invalidToken);
      
      expect(payload).toBeNull();
    });
  });

  describe('isTokenValid', () => {
    test('should return true for valid token', () => {
      // Create a token that expires far in the future
      const futureTime = Math.floor(Date.now() / 1000) + 3600; // 1 hour from now
      const token = 'header.' + btoa(JSON.stringify({ 
        user_id: 'test_user', 
        email: 'test@example.com', 
        exp: futureTime 
      })) + '.signature';
      
      mockLocalStorage.getItem.mockReturnValue(token);
      
      const isValid = TokenManager.isTokenValid();
      expect(isValid).toBe(true);
    });

    test('should return false for expired token', () => {
      // Create a token that expired in the past
      const pastTime = Math.floor(Date.now() / 1000) - 3600; // 1 hour ago
      const token = 'header.' + btoa(JSON.stringify({ 
        user_id: 'test_user', 
        email: 'test@example.com', 
        exp: pastTime 
      })) + '.signature';
      
      mockLocalStorage.getItem.mockReturnValue(token);
      
      const isValid = TokenManager.isTokenValid();
      expect(isValid).toBe(false);
    });

    test('should return false for no token', () => {
      mockLocalStorage.getItem.mockReturnValue(null);
      
      const isValid = TokenManager.isTokenValid();
      expect(isValid).toBe(false);
    });
  });
});
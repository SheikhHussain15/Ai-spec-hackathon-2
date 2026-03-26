/**
 * Authentication Utilities
 *
 * JWT handling for chat API requests.
 */

/**
 * Get JWT token from localStorage
 */
export function getAuthToken(): string | null {
  return localStorage.getItem('token');
}

/**
 * Decode JWT token to extract user ID
 */
export function getUserIdFromToken(token: string): string | null {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.user_id || payload.sub || null;
  } catch (error) {
    console.error('Failed to decode JWT token:', error);
    return null;
  }
}

/**
 * Get current user ID from stored token
 */
export function getCurrentUserId(): string | null {
  const token = getAuthToken();
  if (!token) return null;
  return getUserIdFromToken(token);
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
  const token = getAuthToken();
  if (!token) return false;
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const exp = payload.exp;
    if (!exp) return false;
    
    // Check if token is expired
    const now = Date.now() / 1000;
    return exp > now;
  } catch (error) {
    return false;
  }
}

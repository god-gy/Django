import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import type { User, LoginCredentials } from '@/types/auth';
import { login as apiLogin, logout as apiLogout, getAccessToken, getRefreshToken } from '@/lib/api';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// JWT 토큰에서 사용자 정보 추출
function parseJwt(token: string): { username?: string; user_id?: number; exp?: number } | null {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

function getUserFromToken(token: string | null): User | null {
  if (!token) return null;
  
  const payload = parseJwt(token);
  if (!payload || !payload.user_id) return null;
  
  // 토큰 만료 확인
  if (payload.exp && payload.exp * 1000 < Date.now()) {
    return null;
  }
  
  return {
    username: payload.username || `User ${payload.user_id}`,
  };
}

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // 초기 로드 시 토큰 확인
  useEffect(() => {
    const accessToken = getAccessToken();
    const refreshToken = getRefreshToken();
    
    if (accessToken) {
      const userData = getUserFromToken(accessToken);
      if (userData) {
        setUser(userData);
      } else if (refreshToken) {
        // 액세스 토큰 만료 시 리프레시 토큰으로 재시도할 수 있음
        // 여기서는 단순히 로그아웃 처리
        apiLogout();
      }
    }
    setIsLoading(false);
  }, []);

  const login = useCallback(async (credentials: LoginCredentials) => {
    const tokens = await apiLogin(credentials);
    const userData = getUserFromToken(tokens.access);
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    apiLogout();
    setUser(null);
  }, []);

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}


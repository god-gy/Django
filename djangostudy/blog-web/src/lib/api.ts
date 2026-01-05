import type { Post, PostCreateInput, PostUpdateInput, PaginatedResponse, Comment } from '@/types/post';
import type { TokenPair, LoginCredentials } from '@/types/auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

function normalizeListResponse<T>(data: unknown): T[] {
  if (Array.isArray(data)) return data as T[];
  if (data && typeof data === 'object' && Array.isArray((data as { results?: T[] }).results)) {
    return (data as { results: T[] }).results;
  }
  return [];
}

// 토큰 관리
export const getAccessToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
};

export const getRefreshToken = (): string | null => {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('refresh_token');
};

export const setTokens = (tokens: TokenPair): void => {
  localStorage.setItem('access_token', tokens.access);
  localStorage.setItem('refresh_token', tokens.refresh);
};

export const clearTokens = (): void => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};

// API 요청 헬퍼
async function fetchWithAuth(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const accessToken = getAccessToken();
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (accessToken) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${accessToken}`;
  }

  let response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // 401 에러 시 토큰 갱신 시도
  if (response.status === 401 && getRefreshToken()) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      (headers as Record<string, string>)['Authorization'] = `Bearer ${getAccessToken()}`;
      response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
      });
    }
  }

  return response;
}

// 토큰 갱신
async function refreshAccessToken(): Promise<boolean> {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return false;

  try {
    const response = await fetch(`${API_BASE_URL}/api/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('access_token', data.access);
      return true;
    }
  } catch {
    // 갱신 실패
  }

  clearTokens();
  return false;
}

// 인증 API
export async function login(credentials: LoginCredentials): Promise<TokenPair> {
  const response = await fetch(`${API_BASE_URL}/api/token/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || '로그인에 실패했습니다.');
  }

  const tokens: TokenPair = await response.json();
  setTokens(tokens);
  return tokens;
}

export function logout(): void {
  clearTokens();
}

// Posts API
export interface GetPostsParams {
  limit?: number;
  offset?: number;
}

export async function getPosts(params: GetPostsParams = {}): Promise<PaginatedResponse<Post>> {
  const { limit = 10, offset = 0 } = params;
  const queryParams = new URLSearchParams({
    limit: limit.toString(),
    offset: offset.toString(),
  });
  
  const response = await fetchWithAuth(`/api/posts/?${queryParams}`);
  
  if (!response.ok) {
    throw new Error('포스트 목록을 가져오는데 실패했습니다.');
  }

  const data = await response.json();
  
  // 페이지네이션 응답 형식으로 반환
  if (Array.isArray(data)) {
    return {
      count: data.length,
      next: null,
      previous: null,
      results: data,
    };
  }
  
  return data;
}

export async function getPost(id: number): Promise<Post> {
  const response = await fetchWithAuth(`/api/posts/${id}/`);
  
  if (!response.ok) {
    throw new Error('포스트를 가져오는데 실패했습니다.');
  }

  return response.json();
}

export async function createPost(data: PostCreateInput): Promise<Post> {
  const response = await fetchWithAuth('/api/posts/', {
    method: 'POST',
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || error.title?.[0] || '포스트 생성에 실패했습니다.');
  }

  return response.json();
}

export async function updatePost(id: number, data: PostUpdateInput): Promise<Post> {
  const response = await fetchWithAuth(`/api/posts/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('포스트 수정에 실패했습니다.');
  }

  return response.json();
}

export async function deletePost(id: number): Promise<void> {
  const response = await fetchWithAuth(`/api/posts/${id}/`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error('포스트 삭제에 실패했습니다.');
  }
}

// Comments API
export async function getComments(postId: number): Promise<Comment[]> {
  const response = await fetchWithAuth(`/api/comments/?post_id=${postId}`);

  if (!response.ok) {
    throw new Error('댓글을 불러오는데 실패했습니다.');
  }

  const data = await response.json();
  return normalizeListResponse<Comment>(data);
}

export async function createComment(postId: number, content: string): Promise<Comment> {
  const response = await fetchWithAuth('/api/comments/', {
    method: 'POST',
    body: JSON.stringify({ post: postId, content }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || error.content?.[0] || '댓글 작성에 실패했습니다.');
  }

  return response.json();
}

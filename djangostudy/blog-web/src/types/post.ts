// 백엔드 Post 모델에 맞춘 타입 정의
export interface Post {
  id: number;
  title: string;
  content: string;
  author: number;
  author_username?: string;
  created_at: string;
  updated_at: string;
  comments?: Comment[];
}

export interface Comment {
  id: number;
  content: string;
  author: number;
  post: number;
  created_at: string;
  updated_at: string;
}

export interface PostCreateInput {
  title: string;
  content: string;
}

export interface PostUpdateInput {
  title?: string;
  content?: string;
}

// 페이지네이션 응답 타입
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

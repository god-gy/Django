import { useEffect, useState, type FormEvent } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import type { Post, Comment } from '@/types/post';
import { getPost, deletePost, getComments, createComment } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export default function PostDetailPage() {
  const router = useRouter();
  const { id } = router.query;
  const { isAuthenticated } = useAuth();
  
  const [post, setPost] = useState<Post | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [comments, setComments] = useState<Comment[]>([]);
  const [commentsLoading, setCommentsLoading] = useState(false);
  const [commentsError, setCommentsError] = useState<string | null>(null);
  const [newComment, setNewComment] = useState('');
  const [isSubmittingComment, setIsSubmittingComment] = useState(false);

  useEffect(() => {
    async function fetchPost() {
      if (!id) return;
      
      try {
        const data = await getPost(Number(id));
        setPost(data);
        if (data.comments) {
          setComments(data.comments);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : '포스트를 불러오는데 실패했습니다.');
      } finally {
        setIsLoading(false);
      }
    }

    fetchPost();
  }, [id]);

  useEffect(() => {
    async function fetchComments() {
      if (!id) return;

      setCommentsLoading(true);
      setCommentsError(null);
      try {
        const data = await getComments(Number(id));
        setComments(data);
      } catch (err) {
        setCommentsError(
          err instanceof Error ? err.message : '댓글을 불러오는데 실패했습니다.'
        );
      } finally {
        setCommentsLoading(false);
      }
    }

    fetchComments();
  }, [id]);

  const handleDelete = async () => {
    if (!post || !confirm('정말로 이 포스트를 삭제하시겠습니까?')) return;
    
    setIsDeleting(true);
    try {
      await deletePost(post.id);
      router.push('/');
    } catch (err) {
      alert(err instanceof Error ? err.message : '삭제에 실패했습니다.');
      setIsDeleting(false);
    }
  };

  const handleSubmitComment = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!id) return;

    const content = newComment.trim();
    if (content.length < 10) {
      setCommentsError('댓글은 10자 이상이어야 합니다.');
      return;
    }

    setIsSubmittingComment(true);
    setCommentsError(null);
    try {
      const created = await createComment(Number(id), content);
      setComments((prev) => [created, ...prev]);
      setNewComment('');
    } catch (err) {
      setCommentsError(
        err instanceof Error ? err.message : '댓글 작성에 실패했습니다.'
      );
    } finally {
      setIsSubmittingComment(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[calc(100vh-200px)]">
        <div className="flex items-center gap-3 text-gray-500">
          <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
            <circle 
              className="opacity-25" 
              cx="12" cy="12" r="10" 
              stroke="currentColor" 
              strokeWidth="4" 
              fill="none" 
            />
            <path 
              className="opacity-75" 
              fill="currentColor" 
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" 
            />
          </svg>
          <span>로딩 중...</span>
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <>
        <Head>
          <title>포스트를 찾을 수 없습니다 - Blog</title>
        </Head>
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center py-12 bg-gray-50 rounded-xl">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h2 className="mt-4 text-lg font-medium text-gray-900">{error || '포스트를 찾을 수 없습니다'}</h2>
            <Link
              href="/"
              className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors"
            >
              홈으로 돌아가기
            </Link>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Head>
        <title>{post.title} - Blog</title>
        <meta name="description" content={post.content.slice(0, 160)} />
      </Head>
      
      <article className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* 네비게이션 */}
        <div className="mb-8">
          <Link 
            href="/"
            className="inline-flex items-center gap-2 text-gray-500 hover:text-gray-700 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            목록으로 돌아가기
          </Link>
        </div>

        {/* 포스트 헤더 */}
        <header className="mb-8 pb-8 border-b border-gray-200">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">{post.title}</h1>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4 text-sm text-gray-500">
              <span className="flex items-center gap-2">
                <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center">
                  <svg className="w-4 h-4 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <span className="font-medium text-gray-700">
                  {post.author_username || `작성자 #${post.author}`}
                </span>
              </span>
              <span>·</span>
              <time dateTime={post.created_at} className="flex items-center gap-1">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {formatDate(post.created_at)}
              </time>
            </div>

            {/* 삭제 버튼 (로그인 시에만 표시) */}
            {isAuthenticated && (
              <button
                onClick={handleDelete}
                disabled={isDeleting}
                className="inline-flex items-center gap-1 px-3 py-1.5 text-sm text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50"
              >
                {isDeleting ? (
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                ) : (
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                )}
                삭제
              </button>
            )}
          </div>
        </header>

        {/* 포스트 내용 */}
        <div className="prose prose-lg max-w-none">
          <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
            {post.content}
          </div>
        </div>

        {/* 수정 날짜 */}
        {post.updated_at !== post.created_at && (
          <div className="mt-8 pt-4 border-t border-gray-200">
            <p className="text-sm text-gray-400">
              마지막 수정: {formatDate(post.updated_at)}
            </p>
          </div>
        )}

        {/* 댓글 섹션 */}
        <section className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            댓글 ({comments.length})
          </h2>

          {commentsLoading && (
            <p className="text-sm text-gray-500">댓글을 불러오는 중...</p>
          )}

          {commentsError && (
            <p className="text-sm text-red-600">{commentsError}</p>
          )}

          {!commentsLoading && comments.length === 0 && (
            <p className="text-sm text-gray-500">아직 댓글이 없습니다.</p>
          )}

          {comments.length > 0 && (
            <ul className="mt-6 space-y-4">
              {comments.map((comment) => (
                <li key={comment.id} className="bg-gray-50 rounded-lg p-4">
                  <p className="text-gray-700">{comment.content}</p>
                  <p className="mt-2 text-sm text-gray-500">
                    {formatDate(comment.created_at)}
                  </p>
                </li>
              ))}
            </ul>
          )}

          {isAuthenticated ? (
            <form onSubmit={handleSubmitComment} className="mt-8 space-y-3">
              <label htmlFor="comment" className="block text-sm font-medium text-gray-700">
                댓글 작성
              </label>
              <textarea
                id="comment"
                value={newComment}
                onChange={(event) => setNewComment(event.target.value)}
                rows={4}
                placeholder="댓글을 입력하세요 (10자 이상)"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <button
                type="submit"
                disabled={isSubmittingComment}
                className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-50"
              >
                {isSubmittingComment ? '등록 중...' : '댓글 등록'}
              </button>
            </form>
          ) : (
            <p className="mt-6 text-sm text-gray-500">
              댓글을 작성하려면 로그인하세요.
            </p>
          )}
        </section>
      </article>
    </>
  );
}

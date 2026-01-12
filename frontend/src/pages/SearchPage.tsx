import { useState } from "react";
import FileTable from "../components/FileTable";
import { FileItem, searchFiles } from "../lib/api";

const PAGE_SIZE = 10;

const SearchPage = () => {
  const [query, setQuery] = useState("");
  const [tag, setTag] = useState("");
  const [files, setFiles] = useState<FileItem[]>([]);
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async (newOffset = 0) => {
    setError(null);
    setIsSearching(true);
    try {
      const data = await searchFiles(query, tag, PAGE_SIZE, newOffset);
      setFiles(data.items);
      setTotal(data.total);
      setOffset(newOffset);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("검색에 실패했습니다.");
      }
    } finally {
      setIsSearching(false);
    }
  };

  const canPrev = offset > 0;
  const canNext = offset + PAGE_SIZE < total;

  return (
    <div>
      <h1>파일 검색</h1>
      {error && <div className="error">{error}</div>}
      <div className="card">
        <form
          onSubmit={(event) => {
            event.preventDefault();
            void handleSearch(0);
          }}
        >
          <div>
            <label htmlFor="q">검색어</label>
            <input
              id="q"
              type="text"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="파일명 검색"
            />
          </div>
          <div>
            <label htmlFor="tag">태그</label>
            <input
              id="tag"
              type="text"
              value={tag}
              onChange={(event) => setTag(event.target.value)}
              placeholder="tag"
            />
          </div>
          <button className="primary" type="submit" disabled={isSearching}>
            {isSearching ? "검색 중..." : "검색"}
          </button>
        </form>
      </div>
      <div className="card">
        <h2>검색 결과</h2>
        {isSearching ? (
          <p className="helper">검색 중...</p>
        ) : (
          <FileTable files={files} />
        )}
        <div className="pagination">
          <button
            className="secondary"
            type="button"
            onClick={() => void handleSearch(Math.max(offset - PAGE_SIZE, 0))}
            disabled={!canPrev}
          >
            이전
          </button>
          <span className="helper">
            {total === 0
              ? "0건"
              : `${offset + 1}-${Math.min(offset + PAGE_SIZE, total)} / ${total}건`}
          </span>
          <button
            className="secondary"
            type="button"
            onClick={() => void handleSearch(offset + PAGE_SIZE)}
            disabled={!canNext}
          >
            다음
          </button>
        </div>
      </div>
    </div>
  );
};

export default SearchPage;

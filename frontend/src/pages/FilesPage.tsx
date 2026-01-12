import { useCallback, useEffect, useState } from "react";
import FileTable from "../components/FileTable";
import UploadForm from "../components/UploadForm";
import { deleteFile, downloadUrl, FileItem, listFiles } from "../lib/api";

const PAGE_SIZE = 10;

const FilesPage = () => {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchFiles = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await listFiles(PAGE_SIZE, offset);
      setFiles(data.items);
      setTotal(data.total);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("파일 목록을 불러오지 못했습니다.");
      }
    } finally {
      setIsLoading(false);
    }
  }, [offset]);

  useEffect(() => {
    void fetchFiles();
  }, [fetchFiles]);

  const handleDelete = async (id: number) => {
    const confirmed = window.confirm("이 파일을 삭제할까요?");
    if (!confirmed) {
      return;
    }
    try {
      await deleteFile(id);
      await fetchFiles();
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("삭제에 실패했습니다.");
      }
    }
  };

  const canPrev = offset > 0;
  const canNext = offset + PAGE_SIZE < total;

  return (
    <div>
      <h1>내 파일</h1>
      {error && <div className="error">{error}</div>}
      <div className="card">
        <h2>파일 업로드</h2>
        <UploadForm
          onUploaded={() => {
            setOffset(0);
            void fetchFiles();
          }}
          onError={setError}
        />
      </div>
      <div className="card">
        <h2>파일 목록</h2>
        {isLoading ? (
          <p className="helper">불러오는 중...</p>
        ) : (
          <FileTable files={files} onDelete={handleDelete} downloadBase={downloadUrl} />
        )}
        <div className="pagination">
          <button
            className="secondary"
            type="button"
            onClick={() => setOffset((prev) => Math.max(prev - PAGE_SIZE, 0))}
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
            onClick={() => setOffset((prev) => prev + PAGE_SIZE)}
            disabled={!canNext}
          >
            다음
          </button>
        </div>
      </div>
    </div>
  );
};

export default FilesPage;

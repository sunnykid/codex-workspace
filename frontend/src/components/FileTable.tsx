import { FileItem } from "../lib/api";

const formatBytes = (bytes: number) => {
  if (!Number.isFinite(bytes)) {
    return "-";
  }
  if (bytes === 0) {
    return "0 B";
  }
  const units = ["B", "KB", "MB", "GB"];
  const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  return `${(bytes / 1024 ** index).toFixed(1)} ${units[index]}`;
};

const formatDate = (value: string) => {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString();
};

type FileTableProps = {
  files: FileItem[];
  onDelete?: (id: number) => void;
  downloadBase?: (id: number) => string;
};

const FileTable = ({ files, onDelete, downloadBase }: FileTableProps) => {
  if (files.length === 0) {
    return <p className="helper">표시할 파일이 없습니다.</p>;
  }

  return (
    <table className="table">
      <thead>
        <tr>
          <th>파일명</th>
          <th>용량</th>
          <th>업로드 시간</th>
          <th>태그</th>
          <th>작업</th>
        </tr>
      </thead>
      <tbody>
        {files.map((file) => (
          <tr key={file.id}>
            <td>{file.original_filename}</td>
            <td>{formatBytes(file.size_bytes)}</td>
            <td>{formatDate(file.created_at)}</td>
            <td>{file.tags?.join(", ") || "-"}</td>
            <td>
              <div className="actions">
                {downloadBase && (
                  <a
                    className="secondary"
                    href={downloadBase(file.id)}
                    target="_blank"
                    rel="noreferrer"
                  >
                    다운로드
                  </a>
                )}
                {onDelete && (
                  <button
                    type="button"
                    className="danger"
                    onClick={() => onDelete(file.id)}
                  >
                    삭제
                  </button>
                )}
              </div>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default FileTable;

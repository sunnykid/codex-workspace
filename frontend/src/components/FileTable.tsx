import { FileItem } from "../lib/api";

type Props = {
  files: FileItem[];
  onDelete: (id: number) => void;
  onDownload: (file: FileItem) => void;
};

export default function FileTable({ files, onDelete, onDownload }: Props) {
  return (
    <table>
      <thead>
        <tr>
          <th>파일명</th>
          <th>크기</th>
          <th>태그</th>
          <th>작업</th>
        </tr>
      </thead>
      <tbody>
        {files.map((f) => (
          <tr key={f.id}>
            <td>{f.original_filename}</td>
            <td>{f.size_bytes}</td>
            <td>{(f.tags ?? []).join(", ")}</td>
            <td>
              <button type="button" onClick={() => onDownload(f)}>
                다운로드
              </button>
              <button type="button" onClick={() => {
		      console.log("DEBGU row file object:",f);
		      onDelete(f.id);
	      }}
	      >
                삭제
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}


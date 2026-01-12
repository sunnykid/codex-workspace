import { useState } from "react";
import { uploadFile } from "../lib/api";

const parseTags = (value: string) =>
  value
    .split(",")
    .map((tag) => tag.trim())
    .filter(Boolean);

type UploadFormProps = {
  onUploaded: () => void;
  onError: (message: string) => void;
};

const UploadForm = ({ onUploaded, onError }: UploadFormProps) => {
  const [file, setFile] = useState<File | null>(null);
  const [tagsInput, setTagsInput] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      onError("업로드할 파일을 선택해주세요.");
      return;
    }

    setIsUploading(true);
    try {
      await uploadFile(file, parseTags(tagsInput));
      setFile(null);
      setTagsInput("");
      onUploaded();
    } catch (error) {
      if (error instanceof Error) {
        onError(error.message);
      } else {
        onError("업로드 중 오류가 발생했습니다.");
      }
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="file">파일 선택</label>
        <input
          id="file"
          type="file"
          onChange={(event) => {
            setFile(event.target.files?.[0] ?? null);
          }}
        />
      </div>
      <div>
        <label htmlFor="tags">태그</label>
        <input
          id="tags"
          type="text"
          placeholder="a,b,c"
          value={tagsInput}
          onChange={(event) => setTagsInput(event.target.value)}
        />
        <p className="helper">쉼표로 구분하면 배열로 전송됩니다.</p>
      </div>
      <button className="primary" type="submit" disabled={isUploading}>
        {isUploading ? "업로드 중..." : "업로드"}
      </button>
    </form>
  );
};

export default UploadForm;

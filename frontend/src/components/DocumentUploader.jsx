import { Paperclip } from "lucide-react";

export default function DocumentUploader({ onFiles, files = [] }) {
  return (
    <label className="attach-button" title="Attach incident documents">
      <Paperclip size={16} />
      <span>{files.length ? `${files.length} file${files.length === 1 ? "" : "s"} selected` : "Add photos / documents"}</span>
      <input
        type="file"
        accept="image/jpeg,image/png,image/webp,application/pdf"
        multiple
        onChange={(event) => {
          onFiles?.([...event.target.files]);
          event.target.value = "";
        }}
      />
    </label>
  );
}

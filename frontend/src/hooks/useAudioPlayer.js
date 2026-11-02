import { useCallback, useRef, useState } from "react";

export default function useAudioPlayer() {
  const audioRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const play = useCallback(async (base64, contentType = "audio/mpeg") => {
    if (!base64) return;
    if (audioRef.current) {
      audioRef.current.pause();
      URL.revokeObjectURL(audioRef.current.src);
    }
    const binary = atob(base64);
    const bytes = Uint8Array.from(binary, (char) => char.charCodeAt(0));
    const url = URL.createObjectURL(new Blob([bytes], { type: contentType }));
    const audio = new Audio(url);
    audioRef.current = audio;
    audio.onended = () => {
      URL.revokeObjectURL(url);
      setIsPlaying(false);
    };
    audio.onerror = () => {
      URL.revokeObjectURL(url);
      setIsPlaying(false);
    };
    setIsPlaying(true);
    try {
      await audio.play();
    } catch (error) {
      setIsPlaying(false);
      throw error;
    }
  }, []);
  return { isPlaying, play };
}

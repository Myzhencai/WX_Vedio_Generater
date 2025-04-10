# import os
# import torchaudio
# from FireRedTTS.GenerateVoice import generageVoicemodel
# tts = generageVoicemodel()
# rec_wavs = tts.synthesize(
#         prompt_wav="D:\\Gemini\\FireRedTTS\\examples\\prompt_1.wav",
#         text="为老年人助力，机械外骨骼并非传统机器人。它是一种穿戴式辅助装置，旨在增强老年人的行动能力，减轻身体负担。通过提供额外的支撑和力量，帮助他们更轻松地完成日常活动，提升生活品质，保持独立性，而非完全取代自身机能",
#         lang="zh",
# )
#
# rec_wavs = rec_wavs.detach().cpu()
# out_wav_path = os.path.join("./example.wav")
# torchaudio.save(out_wav_path, rec_wavs, 24000)


import os
import torchaudio
from FireRedTTS.GenerateVoice import generageVoicemodel


def text_to_speech(text_file, output_dir="./output_wavs"):
        tts = generageVoicemodel()

        os.makedirs(output_dir, exist_ok=True)

        with open(text_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

        for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                        continue

                rec_wavs = tts.synthesize(
                        prompt_wav="D:\\Gemini\\FireRedTTS\\examples\\prompt_1.wav",
                        text=line,
                        lang="zh",
                )
                rec_wavs = rec_wavs.detach().cpu()

                output_path = os.path.join(output_dir, f"{i + 1}.wav")
                torchaudio.save(output_path, rec_wavs, 24000)

        return output_dir


# 示例调用
if __name__ == "__main__":
        text_to_speech("Tempfiles/cotant_processed.txt")

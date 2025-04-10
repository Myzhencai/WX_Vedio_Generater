from fireredtts.fireredtts import FireRedTTS

def generageVoicemodel():
    tts = FireRedTTS(
        config_path="D:\\Gemini\\FireRedTTS\\configs\\config_24k.json",
        pretrained_path="D:\\Gemini\\FireRedTTS\\pretrained_models",
    )
    return tts



#
# import os
# import torchaudio
# from fireredtts.fireredtts import FireRedTTS
#
# tts = FireRedTTS(
#     config_path="configs/config_24k.json",
#     pretrained_path="D:\\Gemini\\FireRedTTS\\pretrained_models",
# )
#
# #same language
# rec_wavs = tts.synthesize(
#         prompt_wav="examples/prompt_1.wav",
#         text="小红书，是中国大陆的网络购物和社交平台，成立于二零一三年六月。",
#         lang="zh",
# )
#
# rec_wavs = rec_wavs.detach().cpu()
# out_wav_path = os.path.join("./example.wav")
# torchaudio.save(out_wav_path, rec_wavs, 24000)

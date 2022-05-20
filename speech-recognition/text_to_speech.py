from deeppavlov import build_model, configs

model = build_model(configs.nemo.tts)
filepath_batch = model(["Valid option. I am going to move down."], ['~/move_down.wav'])

print(f'Generated speech has successfully saved at {filepath_batch[0]}')
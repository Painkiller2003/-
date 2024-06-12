from pydub import AudioSegment
from pydub.generators import Sine

def parse_sequence(file_path):
    frequency_duration_pairs = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                data = line.strip('()\n').split(',')
                frequency = None if data[0] == 'None' else float(data[0])
                duration = float(data[1])
                frequency_duration_pairs.append((frequency, duration))
    return frequency_duration_pairs

def create_audio(frequency_duration_pairs, output_path):
    combined = AudioSegment.silent(duration=0)
    for freq, duration in frequency_duration_pairs:
        if freq is not None:
            sine_wave = Sine(freq)
            audio_segment = sine_wave.to_audio_segment(duration=int(duration * 1000))
            combined += audio_segment
        else:
            silence = AudioSegment.silent(duration=int(duration * 1000))
            combined += silence
    combined.export(output_path, format='wav')

# 路径可能需要根据实际情况修改
sequence_path = 'average.txt'
output_audio_path = 'output_audio.wav'

# 解析频率和时长序列
sequence = parse_sequence(sequence_path)

# 生成并保存音频文件
create_audio(sequence, output_audio_path)

print(f"音频文件已生成并保存为：{output_audio_path}")

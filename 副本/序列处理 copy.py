import re
import math
import matplotlib.pyplot as plt

def parse_melody(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    melodies = []
    for line in lines:
        if line.strip():
            notes = re.findall(r'\((.*?)\)', line)
            melody = []
            total_duration = 0
            for note in notes:
                note_info = note.split(',')
                if len(note_info) == 2:
                    pitch = note_info[0].strip()
                    duration = float(note_info[1].strip())  # 改为 float
                    melody.append((pitch, duration))
                    total_duration += duration
                elif len(note_info) == 1:
                    pitch = note_info[0].strip()
                    melody.append((pitch, None))
            melodies.append((melody, total_duration))
    
    return melodies

def pitch_to_cents(pitch):
    if not pitch:
        return None

    base_pitch = 'A0'
    cents_per_semitone = 100
    pitch_order = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note, octave = pitch[:-1], int(pitch[-1])
    base_note, base_octave = base_pitch[:-1], int(base_pitch[-1])
    semitones = (octave - base_octave) * 12 + pitch_order.index(note) - pitch_order.index(base_note)
    cents = semitones * cents_per_semitone
    return cents

def update_melodies(melodies):
    updated_melodies = []
    for melody, total_duration in melodies:
        updated_melody = []
        for pitch, duration in melody:
            if duration is not None and total_duration != 0:
                updated_duration = duration / total_duration
            else:
                updated_duration = None
            updated_melody.append((pitch, updated_duration))
        updated_melodies.append(updated_melody)
    return updated_melodies

def calculate_dynamic_averages(melodies):
    end_times = set()
    for melody in melodies:
        current_time = 0
        for pitch, duration in melody:
            if duration is not None:
                current_time += duration
                end_times.add(current_time)

    end_times = sorted(end_times)
    
    averages = []
    last_time = 0
    for time in end_times:
        sum_cents = 0
        count = 0
        for melody in melodies:
            current_time = 0
            for pitch, duration in melody:
                if duration is not None:
                    if last_time <= current_time < time and current_time + duration >= last_time:
                        if pitch and pitch != '' and pitch_to_cents(pitch) is not None:
                            sum_cents += pitch_to_cents(pitch)
                            count += 1
                    current_time += duration
        average_cents = sum_cents / count if count > 0 else None
        averages.append((last_time, time, average_cents))
        last_time = time

    return averages


def cents_to_frequency(cents):
    f_A0 = 27.500
    if cents is None:
        return None
    return f_A0 * 2 ** (cents / 1200)

def plot_averages(averages):
    plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
    times = [start for start, end, average in averages]
    averages_cents = [average for start, end, average in averages]
    plt.figure(figsize=(10, 6))
    plt.plot(times, averages_cents, marker='o')
    plt.title("平均音分随时间的变化")
    plt.xlabel("时间 (归一化)")
    plt.ylabel("音分 (Cents)")
    plt.grid(True)
    plt.show()

def save_final_sequence(sequence, file_path):
    with open(file_path, 'w') as file:
        for freq, duration in sequence:
            file.write(f"({freq}, {duration:.6f})\n")  # 保留小数点后六位

def main():
    n_seconds = 30  # 你可以设置这个值为任何你需要的秒数
    melodies_path = 'melodies.txt'
    output_path = 'average.txt'
    melodies = parse_melody(melodies_path)
    normalized_melodies = update_melodies(melodies)
    dynamic_averages = calculate_dynamic_averages(normalized_melodies)

    # 计算归一化总持续时间，它应该是1
    normalized_total_duration = sum(end - start for start, end, _ in dynamic_averages)
    # 计算拉伸因子
    stretch_factor = n_seconds / normalized_total_duration

    final_sequence = [(cents_to_frequency(average), (end - start) * stretch_factor) for start, end, average in dynamic_averages]
    print("最终序列 (频率, 时值):")
    for freq, duration in final_sequence:
        print(f"({freq}, {duration:.6f})")
    
    save_final_sequence(final_sequence, output_path)
    plot_averages(dynamic_averages)

if __name__ == "__main__":
    main()

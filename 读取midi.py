import pretty_midi
import os

def midi_number_to_note_name(midi_number):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi_number // 12) - 1
    note_name = note_names[midi_number % 12]
    return f"{note_name}{octave}" if midi_number >= 0 else None

def generate_sequence(midi_file):
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    tempo = midi_data.estimate_tempo()
    beat_length = 60 / tempo  # 每拍的秒数

    events = []

    for instrument in midi_data.instruments:
        for note in instrument.notes:
            start_event = (note.start, note.pitch, 'on')
            end_event = (note.end, note.pitch, 'off')
            events.extend([start_event, end_event])

    events.sort()

    sequence = []
    last_time = 0
    active_notes = {}

    for i, event in enumerate(events):
        time, pitch, event_type = event
        if time > last_time and not active_notes:
            rest_duration = (time - last_time) / beat_length
            if rest_duration > 0:
                sequence.append(('', rest_duration))

        if event_type == 'on':
            active_notes[pitch] = time
        elif event_type == 'off' and pitch in active_notes:
            actual_start_time = active_notes[pitch]
            actual_duration = time - actual_start_time
            note_duration_in_beats = actual_duration / beat_length
            sequence.append((midi_number_to_note_name(pitch), note_duration_in_beats))
            del active_notes[pitch]

        last_time = time

    end_time = midi_data.get_end_time()
    if end_time > last_time and not active_notes:
        final_rest_duration = (end_time - last_time) / beat_length
        sequence.append(('', final_rest_duration))

    return sequence

def process_multiple_midis(midi_folder, output_file):
    midi_files = [os.path.join(midi_folder, f) for f in os.listdir(midi_folder) if f.endswith('.mid')]
    with open(output_file, 'w') as file:
        for midi_file in midi_files:
            sequence = generate_sequence(midi_file)
            sequence_text = ','.join(f"({note if note else ''},{duration:.2f})" for note, duration in sequence)
            file.write(sequence_text + "\n")

# Example usage
midi_folder = 'midi'  # 替换为你的 MIDI 文件夹路径
output_file = 'melodies.txt'  # 输出文件路径
process_multiple_midis(midi_folder, output_file)

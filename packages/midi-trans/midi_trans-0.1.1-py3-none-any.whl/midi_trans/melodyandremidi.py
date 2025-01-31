import midi_tempo_tools
from mido import MidiFile,Message,MidiTrack
import argparse
import os
from musicpy import *
from music21 import converter, stream, note, chord
from collections import defaultdict

def midiRearrange(midi_path,output_path=None,bpm=120):
    midi_tempo_tools.normalize_tempo(midi_path,bpm,midi_path)

    # 设置参数名
    parser = argparse.ArgumentParser()
    # parser.add_argument("-i", dest="midifile", type=str, default=path.name,help='input midifile path')
    # parser.add_argument("-i", dest="midifile", type=str, default='')
    parser.add_argument("-v", dest="velocity", type=int, default='30',help='default 30, less than this value will be removed')
    parser.add_argument("-t", dest="timespan", type=int, default='20',help='default 20, less than this value will be removed')
    parser.add_argument("-s", dest="separate", type=int, default='50',help='default 50, gap between different note_on less than this value will be regarded as strike in the same time')
    parser.add_argument("-c", dest="continue_note", type=int, default='100',help='default 100, gap between the same note_on will be regarded as one')

    # 获取参数
    args = parser.parse_args()

    velocity_threshold = args.velocity #30 #响度阈值
    timeSpan_threshold = args.timespan #20 #持续时间阈值(按下立刻抬起的事件)
    separate_threshold = args.separate #80 #琶音整合阈值
    continue_threshold = args.continue_note

    print ('velocity_threshold:',velocity_threshold)
    print ('timeSpan_threshold:',timeSpan_threshold)
    print ('separate_threshold:',separate_threshold)
    print ('continue_threshold:',continue_threshold)

    try:
        # 直接使用传入的midi_path参数
        mid = MidiFile(midi_path)
        newmid = MidiFile()
        track = MidiTrack()
        # ... existing code ...
    except Exception as e:
        print(f'\r\n无法打开MIDI文件: {str(e)}')
        return None



    onnote = 0
    offnote = 0
    timeline = 0
    onList = []
    pretype = ''

    newmid.ticks_per_beat = mid.ticks_per_beat
    newmid.tracks.append(mid.tracks[0])

    onnote_dict = {}

    tracknum = 1
    try:
        mid.tracks[tracknum]
    except:
        tracknum-=1 
    # 提取按下
    for ttrack in mid.tracks[tracknum]:

        if (ttrack.type=='control_change'):

            timeline += ttrack.time

        elif (ttrack.type=='note_on' or ttrack.type=='note_off'):
            timeline += ttrack.time

            if(ttrack.velocity>velocity_threshold):
                onnote = ttrack.note

                if(onnote in onnote_dict and timeline - onnote_dict[onnote] < continue_threshold and ttrack.velocity< 2*velocity_threshold):
                    onnote_dict[onnote] = timeline
                    continue
                
                onnote_dict[onnote] = timeline
                pretype = 'on'
                ttrack.time = timeline
                track.append(ttrack)
                
            if(ttrack.velocity == 0 or ttrack.type=='note_off'):
                offnote = ttrack.note
                if(pretype=='on' and onnote == offnote and ttrack.time < timeSpan_threshold):
                    del track[len(track)-1]
                pretype = 'off'
        # else:
        #     print ('what?')

    #整和琶音
    timeline = 0
    pretime = 0
    for ttrack in track:
        if(ttrack.time-timeline > separate_threshold):
            timeline = ttrack.time
            pretime = ttrack.time
        else:
            timeline = ttrack.time
            ttrack.time = pretime


    #分离事件
    newtrack = MidiTrack()
    pretime = 0
    keyArea = 1
    #for i in range (0,len(track),1):
    for ttrack in track:
        #ttrack = track[i]
        if(ttrack.time > pretime):#新按下
            pretime = ttrack.time

            if(ttrack.note>=60):#高音区
                keyArea = 1
            else:
                keyArea = 0

            #for j in range (len(onList),0,-1):
            for onnote in onList[::-1]:
                #onnote = onList[j]
                #if((onnote >= 60 and keyArea == 1) or (onnote < 60 and keyArea == 0) ):
                newtrack.append(Message('note_off', channel=0, note=onnote, velocity=0, time=ttrack.time-int(timeSpan_threshold*2)))
                onList.remove(onnote)
            #onList = []
        onList.append(ttrack.note)
        newtrack.append(ttrack)

    #整理时间线
    timeline = 0
    pretime = 0
    for ttrack in newtrack:
        if (ttrack.type=='note_on' or ttrack.type=='note_off'):
            if(ttrack.time>timeline):
                timeline = ttrack.time
                ttrack.time = ttrack.time-pretime
                pretime = timeline
            else:
                ttrack.time = ttrack.time-timeline
            # if(ttrack.time ==0):
            #     ttrack.time = 1

    #补全结束
    for onnote in onList[::-1]:
        newtrack.append(Message('note_off', channel=0, note=onnote, velocity=0, time=2000))

    newmid.tracks.append(newtrack)
    if output_path is None:
        output_path = f"{midi_path[:-4]}remidi.mid"  # 移除.mid后缀并添加remidi.mid

    newmid.save(output_path)
    return output_path


def extract_melody(midi_path, output_path=None):
    # 如果没有指定output_path，则基于midi_path生成
    if output_path is None:
        output_path = f"{midi_path[:-4]}melody.mid"  # 移除.mid后缀并添加melody.mid

    # 读取MIDI文件并合并轨道
    chord_obj, bpm, start_time = read(midi_path).merge()

    # 分离主旋律
    melody = chord_obj.split_melody(
        mode='chord',
        melody_tol=database.minor_seventh,
        chord_tol=database.major_sixth,
        get_off_overlap_notes=True,
        melody_degree_tol='B4'
    )

    # 保存结果
    write(melody, bpm, name=output_path)
    return melody



def highmelody(input_midi,output_midi=None,PITCH_THRESHOLD=30):
    # 输入输出路径
    if output_midi is None:
        output_midi = f"{input_midi[:-4]}_h.mid"  # 移除.mid后缀并添加_h.mid
    # 设置音高阈值（MIDI音符号），低于此值的音符将被视为和弦音并过滤
    # 60是中央C，72是高八度的C
    # 可以根据需要调整这个值
    try:
        # 1. 读取MIDI文件
        print(f"正在读取MIDI文件: {input_midi}")
        score = converter.parse(input_midi)

        # 2. 创建新的声部
        new_part = stream.Part()

        # 3. 按时间收集所有音符
        time_to_notes = defaultdict(list)

        # 收集所有音符和和弦
        for element in score.flat.notesAndRests:
            offset = element.offset

            if isinstance(element, chord.Chord):
                # 从和弦中只获取高于阈值的音符
                for n in element.notes:
                    if n.pitch.midi >= PITCH_THRESHOLD:
                        time_to_notes[offset].append(n)
            elif isinstance(element, note.Note):
                # 只添加高于阈值的单音符
                if element.pitch.midi >= PITCH_THRESHOLD:
                    time_to_notes[offset].append(element)
            else:  # Rest
                time_to_notes[offset].append(element)

        # 4. 对每个时间点只保留最高音
        for offset in sorted(time_to_notes.keys()):
            notes_at_time = time_to_notes[offset]
            if notes_at_time:
                # 过滤出音符（排除休止符）
                actual_notes = [n for n in notes_at_time if isinstance(n, note.Note)]

                if actual_notes:
                    # 只保留最高音
                    highest_note = max(actual_notes, key=lambda n: n.pitch.midi)
                    new_part.insert(offset, highest_note)
                else:
                    # 如果是休止符，保留它
                    rest = next((r for r in notes_at_time if not isinstance(r, note.Note)), None)
                    if rest:
                        new_part.insert(offset, rest)

        # 5. 保存
        final_score = stream.Score()
        final_score.append(new_part)

        print("正在保存简化后的MIDI文件...")
        final_score.write('midi', fp=output_midi)

        print(f"处理完成! 文件已保存为: {output_midi}")

    except Exception as e:
        print(f"处理过程中出错: {str(e)}")














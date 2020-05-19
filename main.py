from playsound import playsound
from termcolor import colored
import glob
import time
import json
import os

os.system('color')

DATASET_OUT_DIR = 'dataset'
TRANSCRIPT_COLORS = {
  'A': 'magenta',
  'B': 'green',
  'C': 'cyan',
  'D': 'white'
}

def GetAllMeetingIDs():
  return [ os.path.basename(folder_path) for folder_path in glob.glob(f'{DATASET_OUT_DIR}/*')]

class Meeting:
  def __init__(self, meeting_id):
    self.meeting_id = meeting_id
    self.meeting_dir = f'{DATASET_OUT_DIR}/{self.meeting_id}'

  def get_audio_path(self):
    return f'{self.meeting_dir}/audio.wav'

  def play_audio(self):
    print(f'\nPlaying {self.meeting_id} ....')
    playsound(self.get_audio_path(), False)

  def print_meeting_metadata(self):
    print(f'\n\n------------ Meeting: {self.meeting_id} --------------')
    with open(f'{self.meeting_dir}/transcript.json') as transcript_json:
      transcripts = json.load(transcript_json)
      speakers = transcripts['speakers']
      for speaker_id, speaker_meta in speakers.items():
        print(f"Speaker ID: {speaker_id}, Global Name: {speaker_meta['global_name']}, Role: {speaker_meta['role']}, Sex: {speaker_meta['sex']}, Age: {speaker_meta['age']}, Native Language: {speaker_meta['native_language']}, Region: {speaker_meta['region']}")

  def get_transcript(self):
    with open(f'{self.meeting_dir}/transcript.json') as transcript_json:
      transcripts = json.load(transcript_json)
      return transcripts['transcript']

  def print_transcript(self):   
    print(f'\n----------- Transcript: {self.meeting_id} -------------')
    timer = time.time() 
    transcripts = self.get_transcript()
    while True:
      is_meeting_ended = False
      for word in transcripts:
        time_escaped = time.time() - timer
        start_time = float(word['start_time'])
        end_time = float(word['end_time'])
        content = word['content']
        speaker_id = word['speaker_id']
        is_punction = bool(word['is_punction'])

        if time_escaped < end_time:
          is_meeting_ended = True        
        if time_escaped <= start_time and time_escaped +1 >= start_time:
          print(colored(f'{speaker_id}: {start_time} {end_time} {content} {"(Punction Mark)" if is_punction else ""}', TRANSCRIPT_COLORS[speaker_id]))
      if not is_meeting_ended:
        break
      time.sleep(1)

  def get_dialog_acts(self):
    with open(f'{self.meeting_dir}/dialog_acts.json') as dialog_acts_json:
      dialog_acts = json.load(dialog_acts_json)
      return dialog_acts['acts']

  def print_dialog_acts(self):
    print(f'\n---------- Dialog Acts: {self.meeting_id} ------------')
    timer = time.time() 
    dialog_acts = self.get_dialog_acts()
    while True:
      is_meeting_ended = False
      for dialog_act in dialog_acts:
        time_escaped = time.time() - timer
        speaker_id = dialog_act['speaker_id']
        act_id = int(dialog_act['id'])
        act = dialog_act['act']
        start_time = float(dialog_act['start_time'])
        end_time = float(dialog_act['end_time'])
        if 'type' in dialog_act:
          main_type = dialog_act['type']['parent']
          sub_type = dialog_act['type']['name']

        if time_escaped < end_time:
          is_meeting_ended = True     
        if time_escaped <= start_time and time_escaped +1 >= start_time:
          print(colored(f'{speaker_id}-{act_id} {main_type}({sub_type}): {start_time} {end_time} {act}', TRANSCRIPT_COLORS[speaker_id]))
      if not is_meeting_ended:
        break
      time.sleep(1)

all_meeting_ids = GetAllMeetingIDs()
for meeting_id in all_meeting_ids:
  meeting = Meeting(meeting_id)
  meeting.print_meeting_metadata()
  meeting.play_audio()
  meeting.print_transcript()
  meeting.play_audio()
  meeting.print_dialog_acts()
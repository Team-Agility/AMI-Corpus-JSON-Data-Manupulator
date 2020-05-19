from playsound import playsound
from termcolor import colored
import glob
import time
import json
import os

os.system('color')

DATASET_OUT_DIR = 'dataset'

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
        starttime = float(word['starttime'])
        endtime = float(word['endtime'])
        content = word['content']
        speaker_id = word['speaker_id']
        is_punction = bool(word['is_punction'])

        if time_escaped < endtime:
          is_meeting_ended = True        
        if time_escaped <= starttime and time_escaped +1 >= starttime:
          print(f'{speaker_id}:', starttime, endtime, content, '(Punction Mark)' if is_punction else '')
      if not is_meeting_ended:
        break
      time.sleep(1)

all_meeting_ids = GetAllMeetingIDs()
for meeting_id in all_meeting_ids:
  meeting = Meeting(meeting_id)
  meeting.print_meeting_metadata()
  meeting.play_audio()
  meeting.print_transcript()
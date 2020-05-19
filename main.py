from playsound import playsound
from termcolor import colored
import argparse
import glob
import time
import json
import sys
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
        main_type = None
        sub_type = None
        if 'type' in dialog_act:
          main_type = dialog_act['type']['main_type']
          sub_type = dialog_act['type']['sub_type']

        if time_escaped < end_time:
          is_meeting_ended = True     
        if time_escaped <= start_time and time_escaped +1 >= start_time:
          print(colored(f'{speaker_id}-{act_id} {main_type}({sub_type}): {start_time} {end_time} {act}', TRANSCRIPT_COLORS[speaker_id]))
      if not is_meeting_ended:
        break
      time.sleep(1)

  def get_extractive_summary(self):
    with open(f'{self.meeting_dir}/extractive_summary.json') as extractive_summary_json:
      extractive_summary = json.load(extractive_summary_json)
      extractive_summary.sort(key=lambda sentence: sentence['dialog_act_start_id'])
      return extractive_summary

  def get_abstractive_summary(self):
    with open(f'{self.meeting_dir}/abstractive_summary.json') as abstractive_summary_json:
      abstractive_summary = json.load(abstractive_summary_json)
      return abstractive_summary

  def print_extractive_summary(self):
    print(f'\n-------- Extractive Summary: {self.meeting_id} ----------')
    ext_summary = self.get_extractive_summary()
    
    for ext_summ_sentence in ext_summary:
      speaker_id = ext_summ_sentence['speaker_id']
      dialog_act = ext_summ_sentence['dialog_act']
      main_type = None
      sub_type = None
      if 'type' in ext_summ_sentence:
          main_type = ext_summ_sentence['type']['main_type']
          sub_type = ext_summ_sentence['type']['sub_type']

      print(colored(f'{speaker_id} - {main_type}({sub_type}): {dialog_act}', TRANSCRIPT_COLORS[speaker_id]))
      time.sleep(2)

  def print_abstractive_summary(self):
    print(f'\n-------- Abstractive Summary: {self.meeting_id} ----------')
    abs_summary = self.get_abstractive_summary()
    
    print(colored('\nAbstract:', 'white', 'on_magenta'))
    for abstract_sentence in abs_summary['abstract']:
      print(colored(f'* {abstract_sentence}', 'yellow'))
    time.sleep(2)

    print(colored('\nActions:', 'white', 'on_magenta'))
    for action_sentence in abs_summary['actions']:
      print(colored(f'* {action_sentence}', 'yellow'))
    time.sleep(2)

    print(colored('\nDecisions:', 'white', 'on_magenta'))
    for decision_sentence in abs_summary['decisions']:
      print(colored(f'* {decision_sentence}', 'yellow'))
    time.sleep(2)

    print(colored('\nProblems:', 'white', 'on_magenta'))
    for problem_sentence in abs_summary['problems']:
      print(colored(f'* {problem_sentence}', 'yellow'))
    time.sleep(2)

  def play_audio_with_transcript(self):
    self.play_audio()
    self.print_transcript()

  def play_audio_with_dialog_atcs(self):
    self.play_audio()
    self.print_dialog_acts()

parser = argparse.ArgumentParser(description='AMI Corpus JSON Data Manupulator')
parser.add_argument('--meetings', help='Meeting ids as comma-separated values')
parser.add_argument('--transcript', action='store_true', help='Play Audio with Transcript')
parser.add_argument('--dialogacts', action='store_true', help='Play Audio with Dialog Acts')
parser.add_argument('--extsummary', action='store_true', help='Play Audio with Extractive Summary')
parser.add_argument('--abssummary', action='store_true', help='Play Audio with Abstractive Summary')

args = parser.parse_args()

# Meetings Args
no_args_present = not (args.transcript or args.dialogacts or args.extsummary or args.abssummary)

all_meeting_ids = GetAllMeetingIDs()
if args.meetings:
  meeting_ids = []
  meeting_ids_args = args.meetings.split(',')
  for meeting_id in meeting_ids_args:
    meeting_id = meeting_id.strip()
    if meeting_id not in all_meeting_ids:
      print(colored(f'Meeting ID {meeting_id} is Invalid', 'red'))
      sys.exit()
    meeting_ids.append(meeting_id)
else:
  meeting_ids = all_meeting_ids

for meeting_id in meeting_ids:
  meeting = Meeting(meeting_id)
  meeting.print_meeting_metadata()
  if args.transcript or no_args_present:
    meeting.play_audio_with_transcript()
  if args.dialogacts or no_args_present:
    meeting.play_audio_with_dialog_atcs()
  if args.extsummary or no_args_present:
    meeting.print_extractive_summary()
  if args.abssummary or no_args_present:
    meeting.print_abstractive_summary()
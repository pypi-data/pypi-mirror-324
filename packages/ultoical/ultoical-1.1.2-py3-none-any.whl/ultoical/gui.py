import os
import tempfile
import uuid

import gradio as gr
from ultoical.ul_handler import ULHandler
from datetime import datetime
from ultoical.ical_handler import ICalHandler
import zipfile

class ULToICALInterface:
  def login_with_password(self, username: str, password: str):
    if self.handler.login_with_password(username, password):
      gr.Info("Login successful / Connection reussie")
    else:
      gr.Warning("There was an error connecting into the account / Une erreur est apparu lors de la connexion")
  def login_with_token(self, token: str):
    self.handler.set_token(token)

  def get_timetables(self, start: float, end: float):
    timetables = self.handler.get_timetables(datetime.fromtimestamp(start), datetime.fromtimestamp(end))
    ret = []
    for timetabl in timetables["plannings"]:
        ret.append(timetabl["label"])
    return gr.CheckboxGroup(choices=ret)

  def makeical(self, timetables):
    files = []
    for timetable in self.handler.get_cached_timetable()["plannings"]:
      if timetable["label"] in timetables:
        ical = ICalHandler(timetable["events"]).make_ical()
        files.append(ical)
        self.tmps.append(ical)
    if len(files) == 1:
      return gr.DownloadButton(value=files[0])
    else:
      file = tempfile.gettempdir() + "/" + str(uuid.uuid4()) + ".zip"
      _zip = zipfile.ZipFile(file, "w", zipfile.ZIP_DEFLATED)
      for file in files:
        _zip.write(file)
      _zip.close()
      self.tmps.append(_zip.filename)
      return gr.DownloadButton(value=_zip.filename)

  def remove_tmps(self):
    for tmp in self.tmps:
        os.remove(tmp)

  def __init__(self):
    self.tmps = []
    self.timetable = None
    self.handler = ULHandler()
    with gr.Blocks() as app:
      gr.Markdown("# ULToICAL")
      with gr.Tab("Login using username and password / Connection via nom d'utilisateur et mot de passe"):
        gr.Markdown(
          "## Log into your account using your username and password")
        gr.Markdown("Se connecter au compte en utilisant un nom d'utilisateur et un mot de passe")
        with gr.Row(equal_height=True):
          self.username = gr.Textbox(label="Your username / Nom d'utilisateur", value="")
          self.password = gr.Textbox(label="Your password / Mot de passe", value="", type="password")
          self.login_button = gr.Button("Login / Connexion")
        self.login_button.click(fn=self.login_with_password, inputs=[self.username, self.password])
      with gr.Tab("Login using token / Connection par jeton"):
        gr.Markdown("## Log into your account using token (More info [here](https://github.com/totorocodesoften/ultoical/readme.md))")
        gr.Markdown("Se connecter au compte en utilisant un jeton (Plus d'informations [ici](https://github.com/totorocodesoften/ultoical/readme.fr.md)")
        with gr.Row(equal_height=True):
          self.token = gr.Textbox(label="Your token / Votre jeton", value="")
          self.login_button = gr.Button("Login / Connexion")
        self.login_button.click(fn=self.login_with_token, inputs=[self.token])
      gr.Markdown("## Choose dates")
      gr.Markdown("Choisissez les dates")
      with gr.Row(equal_height=True) as self.period:
        with gr.Column():
          self.start = gr.DateTime(label="Start of the period / Debut de la periode", include_time=False)
        with gr.Column():
            self.end = gr.DateTime(label="End of the period / Fin de la periode", include_time=False)
        self.get_timetables_button = gr.Button("Get timetables / Obtenir les emplois du temps")
      gr.Markdown("## Timetables")
      gr.Markdown("Emploi du temps")
      self.timetable = gr.CheckboxGroup(label="Timetable / Emplois du temps", info="If none are there the connection failed / Si aucun n'est apparu il y a eu un probleme de connexion")
      self.get_timetables_button.click(fn=self.get_timetables, inputs=[self.start, self.end], outputs=[self.timetable])
      gr.Markdown("## Download")
      gr.Markdown("Telechargement")
      dwnbtn = gr.DownloadButton()
      self.timetable.input(fn=self.makeical, inputs=[self.timetable], outputs=[dwnbtn])
      dwnbtn.click(fn=self.remove_tmps)
    app.launch()

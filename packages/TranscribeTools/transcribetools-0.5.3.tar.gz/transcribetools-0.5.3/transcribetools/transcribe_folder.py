import time
from pathlib import Path
# import tkinter as tk
from tkinter.filedialog import askdirectory
# from tkinter import messagebox as mb
import pymsgbox as msgbox
# import toml
import whisper
# import rich
from rich.prompt import Prompt
import rich_click as click
from result import Result, is_ok, is_err, Ok, Err  # noqa: F401
import soundfile as sf
from .transcribe_folder_model import save_config_to_toml, get_config_from_toml, show_config, console

# logging.getLogger("python3").setLevel(logging.ERROR)
# loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
# tk bug in sequoia
# import sys
# sys.stderr = open("log", "w", buffering=1)
# can't find the 'python3' logger to silence

MODEL = "large"
# LOCALPATH = ('/Users/ncdegroot/Library/CloudStorage/'
#              'OneDrive-Gedeeldebibliotheken-TilburgUniversity/'
#              'Project - Reflective cafe - data')
LOCALPATH = Path.cwd()
model = None


def process_file(path, args):
    output_path = path.with_suffix('.txt')
    try:
        click.echo("Start processing...")
        result = model.transcribe(str(path),
                                  verbose=True,
                                  **args,)
        # false: only progressbar; true: all; no param: no feedback
    except Exception as e:
        click.echo(f"Error while processing {path}: '{e}'. Please fix it")
    else:
        text_to_save = result["text"]
        click.echo(text_to_save)

        # file_name = f"{data_file.split('.')[0]}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"
        # file_name = output_path
        # Open the file in write mode
        with open(output_path, 'w') as file:
            # Write the text to the file
            file.write(text_to_save)

        click.echo(f'Text has been saved to {output_path}')


@click.group(no_args_is_help=True,
             epilog='Use config --help or process --help to see options.\n'
                    'Check out the docs at https://gitlab.uvt.nl/tst-research/transcribetools '
                    'for more details')
@click.version_option(package_name='transcribetools')
@click.option('--debug/--no-debug',
              '-d/-n',
              help="Print debug messages and timing information",
              default=False)
@click.pass_context  # our 'global' context
@click.option("--configfilename",
              '-c',
              default=Path.home()/"localwhisper.toml",
              help="Specify config file to use",
              # show_default=True,
              metavar="FILE",
              type=click.Path(exists=True, dir_okay=False, readable=True, resolve_path=True),
              show_choices=False,
              required=False,
              # prompt="Enter new config filename or accept default",
              )
def cli(ctx: click.Context, debug, configfilename):
    global model
    # open config, ask for values if needed:
    #  Prompt.ask(msg)
    home = Path.home()
    config_path = home / configfilename
    if debug:
        click.echo(f"Config_path: {config_path}")
    if not config_path.exists():
        save_config_to_toml(config_path, LOCALPATH, MODEL)
    result = get_config_from_toml(config_path)  # has the default values (homedir, large)
    if is_err(result):
        click.echo(f"Exiting due to {result.err}")
        exit(1)
    config = result.ok_value
    if config:
        # click.echo("Config")
        click.echo(f"Config filename: {config_path}")
        # click.echo(f"Folder path for soundfiles: {config.folder}")
        # click.echo(f"Transcription model name: {config.model}")
    config.debug = debug
    ctx.obj = config
    # process_files(config)


# the `cli` subcommand 'process'

@cli.command("process", help="Using current configuration, transcribe all soundfiles in the folder")
@click.option('--language',
              '-l',
              default="AUTO",
              type=click.Choice(['NL', 'UK', 'AUTO'],
                                case_sensitive=False,
                                ))
@click.option('--prompt',
              '-p',
              help='-p "" You can add special prompts and words (spelling) (max 224 chars) see '
                   'https://cookbook.openai.com/examples/whisper_prompting_guide')
@click.pass_obj  # in casu the config obj
def process(config, prompt, language):
    global model
    # config = config
    if config.debug:
        click.echo(f"Load model: {config.model}")
    model = whisper.load_model(config.model)
    soundfiles_path = Path(config.folder)
    if config.debug:
        click.echo(f"Folder path for soundfiles: {soundfiles_path}")
        click.echo(f"{language=}, {prompt=} ")

    txt_files = [file for file in soundfiles_path.glob('*') if file.suffix.lower() == '.txt']
    file_stems = [file.stem for file in txt_files]
    # a txt file_stem indicates mp3 has been processed already
    soundfiles = [file for file in soundfiles_path.glob('*') if file.suffix.lower()
                  in '.mp3mp3.mp4.mpweg.mpga.m4a.wav.webm' and file.stem not in file_stems]
    click.echo(f"{len(soundfiles)} files to be processed")
    duration = 0
    start = time.perf_counter()

    for file in soundfiles:
        f, samplerate = sf.read(file)
        duration += len(f) / samplerate
        click.echo(f"Processing {file}")
        args = dict()
        if language != "AUTO":
            args["language"] = language
        if prompt:
            args["prompt"] = prompt
        process_file(file, args)
    if soundfiles:
        process_time = time.perf_counter() - start
        click.echo(f"Total sound duration: {duration:.1f} seconds, \n"
                   f"processing time: {process_time:.1f} seconds, \n"
                   f"realtime factor: {(process_time/duration):.2f}")


# the `cli` command config
@cli.group("config", help="configuration")
def config():
    pass


# the `config` create subcommand
@click.command("create", help="Create new configuration file")
def create():
    msg = "Select folder to containing the sound files"
    click.echo(msg)
    # root = tk.Tk()
    # root.focus_force()
    # Cause the root window to disappear milliseconds after calling the filedialog.
    # root.after(100, root.withdraw)
    # tk.Tk().withdraw()
    # hangs: mb.showinfo("msg","Select folder containing the sound files")
    msgbox.alert(msg, "info")
    # "title" only supported on linux ith wv ...
    folder = askdirectory(title="Select folder to monitor containing the sound files",
                          mustexist=True,
                          initialdir='~')
    choices = ["tiny", "base", "small", "medium", "large", "turbo"]
    # inx = ask_choice("Choose a model", choices)
    # model = choices[inx]
    model = Prompt.ask("Choose a model",
                       console=console,
                       choices=choices,
                       show_default=True,
                       default="large")
    config_name = Prompt.ask("Enter a name for the configuration file",
                             show_default=True,
                             default="localwhisper.toml")
    config_path = Path(config_name)
    toml_path = config_path.with_suffix(".toml")
    while toml_path.exists():  # current dir
        result = get_config_from_toml(toml_path)
        click.secho("Already exists...", fg='red')
        show_config(result)
        overwrite = Prompt.ask("Overwrite?",
                               choices=["y", "n"],
                               default="n",
                               show_default=True)
        if overwrite == "y":
            break
        else:
            return
    # Prompt.ask("Enter model name")
    save_config_to_toml(toml_path, folder, model)
    click.echo(f"{toml_path} saved")


# the 'config' show subcommand
@click.command("show", help="Show current configuration file")
@click.pass_obj
def show(config):
    click.echo(f"Config folder path: {config.folder}")
    click.echo(f"Config model name: {config.model}")


# connect the subcommand to `config'
config.add_command(create)
config.add_command(show)

if __name__ == "__main__":
    cli()

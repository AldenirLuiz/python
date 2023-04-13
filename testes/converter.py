import argparse, re
from os import path, getcwd, mkdir, listdir, devnull
from subprocess import Popen

# valida se 'string' segue o padrão de resolução de tela. 9999x9999 ou 9999X9999
def isScreenSize(string):
    regex = re.compile(r"^\d+x\d+$", re.IGNORECASE)
    if not regex.match(string):
        raise argparse.ArgumentTypeError("Formato de resolucao de tela invalido! - Padrao: \"640x360\"")
    
    return string


# cria o parser de argumentos
parser = argparse.ArgumentParser(description=u"Converte todos os arquivos de video de uma pasta.")

#tipos de conversao
parser.add_argument("-f", "--flv", action="store_true", help=u"Faz a conversão do arquivo original para o formato FLV.")
parser.add_argument("-m", "--mp4", action="store_true", help=u"Faz a conversão do arquivo original para o formato MP4.")
parser.add_argument("-w", "--webm", action="store_true", help=u"Faz a conversão do arquivo original para o formato WEBM.")

#propriedades
parser.add_argument("-s", "--size", default="640x360", type=isScreenSize, help=u"Resolução de saída dos vídeos. Valor padrao: '640x360'")
parser.add_argument("-t", "--type", default="mp4", help=u"Extensão dos arquivos que serão convertidos. Valor padrao: 'mp4'")
parser.add_argument("-d", "--directory", default="converted_videos", help=u"Diretório que conterá os vídeos convertidos. Valor padrao: 'converted_videos'")

#argumento obrigatorio
parser.add_argument("path", help=u"Pasta onde estão os arquivos a serem convertidos.")

#le os argumetos recebidos
args = parser.parse_args();

#recebe o path, se não existir lanca a ajuda e depois sai do sistema
root_path = path.join(args.path)
if not path.exists(root_path):
    error_message = ""
    parser.print_help()
    print ("\n--------------------------------------------------------------------------\n")
    error_message = path.abspath(root_path) + ": pasta não existe!\n"
    parser.exit(status=1, message=error_message)

#pasta onde ficarao os arquivos convertidos
converted_path = path.join(root_path, args.directory)

# se nao existir cria a pasta
if not path.exists(converted_path):
    mkdir(converted_path)

# lista de arquivos que serao convertidos
file_list = []

# pesquisa na pasta por arquivos que tenham a extensao --type (mp4 padrao)
for arquivo in listdir(root_path):
    if arquivo.endswith("." + args.type):
        file_list.append(arquivo)

print ("=== Pasta de origem:  ", path.abspath(root_path))
print ("=== Pasta de destino: ", path.abspath(converted_path))
print ("")
print ("====================== Arquivos encontrados ======================" if file_list else "=== Nenhum arquivo encontrado!")
for arquivo in file_list:
    print (" - ", path.abspath(path.join(root_path, arquivo)))

print ("==================================================================\n" if file_list else "\n")

FNULL = open(devnull, 'w')

if args.flv:
    command_args = [
        'ffmpeg', 
        '-i', 
        None, #index 2
        '-vcodec', 
        'libx264', 
        '-preset', 
        'slower', 
        '-profile', 
        'baseline', 
        '-x264opts', 
        'bitrate=500', 
        '-s', 
        args.size, 
        '-crf', 
        '26', 
        '-g', 
        '12', 
        '-acodec', 
        'libmp3lame', 
        '-ar', 
        '44100', 
        '-f', 
        'flv',
        None #index 23
    ]

    for arquivo in file_list:
        command_args[2] = path.abspath(path.join(root_path, arquivo))
        command_args[23] = path.abspath(path.join(converted_path, arquivo[:-3] + "flv"))
        
        print ("=== '" + arquivo + "' (MP4->FLV)")
        print (" - Comando: ", " ".join(command_args))
        print (" - Convertendo...")
        
        proc = Popen(command_args, stdout=FNULL, stderr=FNULL)
        proc.communicate()
        print (" - Falha na conversao!" if proc.returncode != 0 else " - Conversao completa!")
        print ("")


if args.webm:
    command_args = [
        'ffmpeg',
        '-i',
        None, #index 2
        '-acodec',
        'libvorbis',
        '-qscale:a',
        '4',
        '-ar',
        '44100',
        '-b',
        '345k',
        '-s',
        args.size,
        '-qmax',
        '26',
        None #index 15
    ]

    for arquivo in file_list:
        command_args[2] = path.abspath(path.join(root_path, arquivo))
        command_args[15] = path.abspath(path.join(converted_path, arquivo[:-3] + "webm"))
        
        print ("=== '" + arquivo + "' (MP4->WEBM)")
        print (" - Comando: ", " ".join(command_args))
        print (" - Convertendo...")
        
        proc = Popen(command_args, stdout=FNULL, stderr=FNULL)
        proc.communicate()
        print (" - Falha na conversao!" if proc.returncode != 0 else " - Conversao completa!")
        print ("")

if args.mp4:
    command_args = [
        'ffmpeg', 
        '-i', 
        None, #index2
        '-vcodec', 
        'libx264', 
        '-preset', 
        'slower', 
        '-profile', 
        'baseline', 
        '-x264opts', 
        'bitrate=500', 
        '-s', 
        args.size, 
        '-crf', 
        '26', 
        '-g', 
        '12', 
        '-c:a', 
        'libvo_aacenc', 
        '-b:a', 
        '128k', 
        '-f', 
        'mp4', 
        None #index 23
    ]

    for arquivo in file_list:
        command_args[2] = path.abspath(path.join(root_path, arquivo))
        command_args[23] = path.abspath(path.join(converted_path, arquivo))
        
        print ("=== '" + arquivo + "' (MP4->MP4)")
        print (" - Comando: ", " ".join(command_args))
        print (" - Convertendo...")
        
        proc = Popen(command_args, stdout=FNULL, stderr=FNULL)
        proc.communicate()
        print (" - Falha na conversao!" if proc.returncode != 0 else " - Conversao completa!")
        print ("")



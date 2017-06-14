
from __future__ import print_function
import argparse
import os,os.path

randomString = "hstRGYERHdf43#@^%&!" # Obtained by fair die roll. Guaranteed to be random.

def unpack(pathToPackedText='packedText.txt'):
  with open(pathToPackedText, 'r') as packedFile:
    #lines = packedFile.readlines()
    sep = packedFile.readline() # include \n
    if sep != randomString + '\n':
      raise RuntimeError("separator has changed, be very sure you know what you're doing")
    packedText = packedFile.read()
    files = packedText.split(sep)
    for contentWithName in files:
      name,content = contentWithName.split('\n', 1)
      assert name[-4:] == '.txt'
      print('about to unpack', name)
      if os.path.exists(name):
        raise RuntimeError("text file {} is already present in {}, halt and catch fire".format(name, os.getcwd() ) )
      else:
        open(name, 'w').write(content)

def pack(directory=os.getcwd(), packedFileName='packedText.txt'):
  files = list()
  #for (dirpath, dirnames, filenames) in os.walk(directory):
  #  assert dirpath == directory
  #  for filename in filenames:
  for filename in os.listdir(directory):
      if filename[-4:] == '.txt' and filename != packedFileName:
        print('packing', filename)
        contents = open(filename, 'r').read()
        files.append( (filename, contents) )
  with open(packedFileName, 'w') as packedFile:
    packedFile.write(''.join([randomString + '\n' + filename + '\n' + contents for filename,contents in files]) )




if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('directory', nargs='?',
                      #default=os.getcwd(),
                      help='path to the directory to pack all the text files from')
  parser.add_argument('--unpack',
                      #default='packedText.txt',
                      help='path to file to unpack')
  args = parser.parse_args()
  if args.directory is not None and args.unpack is not None:
    raise ValueError('Please only pack or unpack.')
  if args.unpack is not None:
    unpack(args.unpack)
  elif args.directory is not None:
    pack(args.directory)

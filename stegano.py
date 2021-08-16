"""
Stegano.py
https://github.com/MatMasIt/steganoCode

2021, Mattia Mascarello
"""

import argparse
import os
import sys
import re

def unicodeToBin(text):
    return ''.join('{:08b}'.format(b) for b in text.encode('utf8'))
def binToUnicode(binI):
    return bytes(int(b, 2) for b in re.split('(........)', binI) if b).decode('utf8')
def binToRTLLTR(binI):
    final = ""
    for b in list(binI):
        if b == "1":
            final += "\u200f" # RTL
        else:
            final += "\u200e" # LTR
    if final[-1] == "\u200f":
        final += "\u200e"
    else:
        final += "\u200f"
    return final
def RTLLTRToBin(rtlltr):
    final = ""
    for c in list(rtlltr):
        if c == "\u200f":
            final+="1"
        else:
            final+="0"
    final= final [:-1]
    return final
    
    
def enc(message):
    return binToRTLLTR(unicodeToBin(message))
    
def dec(encoded):
    return binToUnicode(RTLLTRToBin(encoded))
    
def multilineComment(message,comment,begin="\n/*\n",end="\n*/\n"):
    final = begin
    final += enc(message)
    final += "\n"+comment+"\n"
    final += end
    return final

def srcEnc(src,lang,message,comment):
    if lang == "py":
        comm = multilineComment(message,comment,'\n"""\n','\n"""\n')+"\n"+src
    else:
        comm = multilineComment(message,comment)+"\n"+src
    return comm

def srcDec(src):
    found=[]
    accumulator="" 
    srcPrev=""
    for char in list(src):
        if char == "\u200f" or char == "\u200e":
            accumulator+=char
        elif len(accumulator):
            accumulator=dec(accumulator)
            srcPrev+=accumulator
            srcPrev+=char
            found.append(accumulator)
            accumulator=""
        else:
           srcPrev+=char
    res={"found":found,"cleanedSrc":srcPrev}
    return res
          
    

parser = argparse.ArgumentParser()
parser.add_argument("--input", help="Input file")
parser.add_argument("--output", help="Output file")
parser.add_argument("--stdin", action='store_true', help="Read from stdin")
parser.add_argument("--stdout", action='store_true', help="Output to stdout")
parser.add_argument("--hide", action='store_true', help="Hide Mode")
parser.add_argument("--showSource", action='store_true', help="Show clean source")
parser.add_argument("--showFound", action='store_true', help="Show Matches")
parser.add_argument("--lang", help="Programming Language")
parser.add_argument("--message", help="Hidden message")
parser.add_argument("--comment", help="Comment")

args = parser.parse_args()

if args.input:
    if not os.path.isfile(args.input):
        sys.exit("You must specify a valid input file")
    try:
        data=open(args.input,"r").read()
    except:
        sys.exit("Could not read file")
elif args.stdin:
    data = ""
    for line in sys.stdin:
        data+=line
else:
    sys.exit("No input method")

if not args.output and not args.stdout:
    sys.exit("No output method")


if args.hide:
    if args.message and len(args.message):
        if args.lang:
            if args.comment:
                comment=args.comment
            else:
                comment=""
            res=srcEnc(data,args.lang,args.message,comment)
            if args.output:
                out=open(args.output,"w+")
                out.write(res)
                out.close()
            if args.stdout:
                print(res)
        else:
            sys.exit("Specify a language")
    else:
        sys.exit("Specifify a message")
elif args.showSource or args.showFound:
    res=srcDec(data)
    if args.showSource:
        r=res["cleanedSrc"]
    else:
       r="\n".join(res["found"])
    if args.output:
        out=open(args.output,"w+")
        out.write(r)
        out.close()
    if args.stdout:
        print(r)
else:
    sys.exit("No action specified")

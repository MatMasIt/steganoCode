# steganoCode
Steganography in source code

```
usage: stego.py [-h] [--input INPUT] [--output OUTPUT] [--stdin] [--stdout] [--hide] [--showSource] [--showFound]
                [--lang LANG] [--message MESSAGE] [--comment COMMENT]

optional arguments:
  -h, --help         show this help message and exit
  --input INPUT      Input file
  --output OUTPUT    Output file
  --stdin            Read from stdin
  --stdout           Output to stdout
  --hide             Hide Mode
  --showSource       Show clean source
  --showFound        Show Matches
  --lang LANG        Programming Language
  --message MESSAGE  Hidden message
  --comment COMMENT  Comment

```

This tools encodes secret messages in a comment, which is appended at the start of the output


## Encoding

The message is first commuted from unicode to binary and then to a sequence of these two invisible unicode characters:
* `U+200F RIGHT-TO-LEFT MARK` for binary digit `1`
* `U+200E LEFT-TO-RIGHT MARK` fot binary digit `0`

The last char in the sequence is always ignored in decoding and is `U+200F RIGHT-TO-LEFT MARK` (to restore the correct reading order that the previous char would impart)
A comment is created, accounting for the programming language and placed at the top of the output.
The comment contains the message payload followed optionally by a text comment

## Decoding

Every sequence of the two designated chars is stored and decoded.

if `showSource` is enabled, then the source output contains the original message in the comments where it appears
if `showFound` is enabled, the output contains all the decoded instances


### example
[![asciicast](https://asciinema.org/a/430713.svg)](https://asciinema.org/a/430713)

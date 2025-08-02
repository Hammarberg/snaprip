#!/usr/bin/env python3

"""
snaprip v1.00 [12.02.2022] *** by fieserWolF
usage: snaprip.py [-h] snapshot output

This script parses C64 Vice snapshots and extracts font, graphics and petscii from it.

positional arguments:
  snapshot    snapshot file
  output      output filename

optional arguments:
  -h, --help  show this help message and exit

Example: ./snaprip.py snapshot.vsf test
"""

import os
import sys
import argparse
import struct


PROGNAME = 'snaprip';
VERSION = '2.00';
DATUM = '27.02.2022';

#see https://vice-emu.sourceforge.io/vice_9.html#SEC255

#OFFSET_VICE_VERSION = 0x0016
#OFFSET_HEADER = 0x0016          #every header: 16+1+1+4=22 = $16
OFFSET_CIA = 0x0000
OFFSET_RAM = 0x0004
OFFSET_COLRAM = 0x02f9
OFFSET_VIC = 0x0001

SIZE_C64_MEMORY = 65536
SIZE_C64_VIC    = 48
SIZE_C64_CIA2   = 15
SIZE_C64_COLRAM = 1000

snapshot = []
filepos = 0


c64_memory = []
c64_vic = []
c64_cia2 = []
c64_colram = []

value_d011 = 0
value_d015 = 0
value_d016 = 0
value_d018 = 0
value_d020 = 0
value_d021 = 0
value_dd00 = 0

addr_vicbank = 0
addr_bitmap = 0
addr_screen = 0
addr_font = 0

value_sprite1_pointer = 0
value_sprite2_pointer = 0
value_sprite3_pointer = 0
value_sprite4_pointer = 0
value_sprite5_pointer = 0
value_sprite6_pointer = 0
value_sprite7_pointer = 0
value_sprite8_pointer = 0

value_sprite1_memory = 0
value_sprite2_memory = 0
value_sprite3_memory = 0
value_sprite4_memory = 0
value_sprite5_memory = 0
value_sprite6_memory = 0
value_sprite7_memory = 0
value_sprite8_memory = 0

mode_bitmap = False
mode_multicolor = False
mode_custom_font = False



def _load_some_data (
    filename
) :
	#open input file
    print ('Opening file "%s" for reading...' % filename)
    try:
        file_in = open(filename , 'rb')
    except IOError as err:
        print('I/O error: {0}'.format(err))
        return None

    buffer=[]
    while True:
        data = file_in.read(1)  #read 1 byte
        if not data: break
        temp = struct.unpack('B',data)
        buffer.append(temp[0])

    return buffer




def _save_some_data(
    filename,
    data
):
    print ('Opening file "%s" for writing data (%d ($%04x) bytes)...' % (filename, len(data), len(data)))
    try:
        file_out = open(filename , 'wb')
    except IOError as err:
        print('I/O error: {0}'.format(err))
        return None
    file_out.write(bytearray(data))
    file_out.close()


def _process() :
    """
        https://www.c64-wiki.de/index.php/VIC
        interessant:
        $d011 (mode)
        $d016 (multicolor/hires)
        $d018 (speicherpointer screen/font(bitmap))
        $d020 (rahmenfarbe)
        $d021 (hintergrundfarbe)

        https://www.c64-wiki.de/index.php/CIA
        interessant:
        $DD00 = %xxxxxx11 -> bank0: $0000-$3fff
        $DD00 = %xxxxxx10 -> bank1: $4000-$7fff
        $DD00 = %xxxxxx01 -> bank2: $8000-$bfff
        $DD00 = %xxxxxx00 -> bank3: $c000-$ffff
    """
    
    global value_d011, value_d015, value_d016, value_d018, value_d020, value_d021, value_dd00
    global value_sprite1_memory, value_sprite2_memory, value_sprite3_memory, value_sprite4_memory, value_sprite5_memory, value_sprite6_memory, value_sprite7_memory, value_sprite8_memory
    global value_sprite1_pointer, value_sprite2_pointer, value_sprite3_pointer, value_sprite4_pointer, value_sprite5_pointer, value_sprite6_pointer, value_sprite7_pointer, value_sprite8_pointer
    global mode_bitmap, mode_custom_font, mode_multicolor
    global addr_bitmap, addr_font, addr_screen, addr_vicbank

    value_d011 = c64_vic[0x0011]
    value_d015 = c64_vic[0x0015]
    value_d016 = c64_vic[0x0016]
    value_d018 = c64_vic[0x0018]
    value_d020 = c64_vic[0x0020]
    value_d021 = c64_vic[0x0021]
    value_dd00 = c64_cia2[0x0000]

    # shamelessly taken from vicegrab.c
    addr_vicbank = 0xc000 - (value_dd00 & 0b00000011) * 0x4000
    addr_bitmap = ((value_d018 >> 3) & 0b00000001) * 0x2000 + addr_vicbank
    addr_font = ((value_d018 >> 1) & 0b00000111) * 0x0800 + addr_vicbank 
    addr_screen = (value_d018 >> 4) * 0x0400 + addr_vicbank

    # check if bitmap mode (0xd011 bit 5)
    mode_bitmap = False
    if ( (value_d011 & 0b00100000) != 0 ) : mode_bitmap = True

    # check if multicolor mode (0xd016 bit 4)
    mode_multicolor = False
    if ( (value_d016 & 0b00010000) != 0 ) : mode_multicolor = True

    # check if custom font (font not 0x1xxx or 0x9xxx)
    mode_custom_font = True
    if (
        (addr_font == 0x1000) |
        (addr_font == 0x1800) |
        (addr_font == 0x9000) |
        (addr_font == 0x9800)
    ) : mode_custom_font = False

    value_sprite1_pointer = c64_memory[addr_screen+0x03f8+0]
    value_sprite1_memory = addr_vicbank + value_sprite1_pointer*64
    value_sprite2_pointer = c64_memory[addr_screen+0x03f8+1]
    value_sprite2_memory = addr_vicbank + value_sprite2_pointer*64
    value_sprite3_pointer = c64_memory[addr_screen+0x03f8+2]
    value_sprite3_memory = addr_vicbank + value_sprite3_pointer*64
    value_sprite4_pointer = c64_memory[addr_screen+0x03f8+3]
    value_sprite4_memory = addr_vicbank + value_sprite4_pointer*64
    value_sprite5_pointer = c64_memory[addr_screen+0x03f8+4]
    value_sprite5_memory = addr_vicbank + value_sprite5_pointer*64
    value_sprite6_pointer = c64_memory[addr_screen+0x03f8+5]
    value_sprite6_memory = addr_vicbank + value_sprite6_pointer*64
    value_sprite7_pointer = c64_memory[addr_screen+0x03f8+6]
    value_sprite7_memory = addr_vicbank + value_sprite7_pointer*64
    value_sprite8_pointer = c64_memory[addr_screen+0x03f8+7]
    value_sprite8_memory = addr_vicbank + value_sprite8_pointer*64

    print('processing...')
    print(' addr_vicbank = $%04x' %(addr_vicbank))
    print(' addr_bitmap = $%04x' %(addr_bitmap))
    print(' addr_screen = $%04x' %(addr_screen))
    print(' addr_font = $%04x' %(addr_font))
    print(' $d011 = $%04x %%%s' %(value_d011,format(value_d011,"08b")))
    print(' $d015 = $%04x %%%s' %(value_d015,format(value_d015,"08b")))
    print(' $d016 = $%04x %%%s' %(value_d016,format(value_d016,"08b")))
    print(' $d018 = $%04x %%%s' %(value_d018,format(value_d018,"08b")))
    print(' $d020 = $%04x' %(value_d020))
    print(' $d021 = $%04x' %(value_d021))
    # print(' value_sprite1_pointer = %04x' %(value_sprite1_pointer))
    print(' value_sprite1_memory = $%04x' %(value_sprite1_memory))
    print(' value_sprite2_memory = $%04x' %(value_sprite2_memory))
    print(' value_sprite3_memory = $%04x' %(value_sprite3_memory))
    print(' value_sprite4_memory = $%04x' %(value_sprite4_memory))
    print(' value_sprite5_memory = $%04x' %(value_sprite5_memory))
    print(' value_sprite6_memory = $%04x' %(value_sprite6_memory))
    print(' value_sprite7_memory = $%04x' %(value_sprite7_memory))
    print(' value_sprite8_memory = $%04x' %(value_sprite8_memory))
    print('processing done.')
    print()




def _values_to_ascii (
    values
):
    return_string = ''
    for i in values :
        if (i != 0) : return_string += chr(i)
    return return_string.strip()

    

def _values_to_number (
    values
):
    return_number = 0
    multi = 1
    for i in values :
        return_number += i*multi
        #print('i=%d, multi=%d, number=%i' %(i,multi,return_number))
        multi *= 256
    return return_number
    


def _check_snapshot_header() :
    global filepos

    PRE_MAGIC = 'VICE Snapshot File' #+0x1a
    PRE_MACHINE = 'C64SC'
    PRE_VERSION_MAJOR = 2
    PRE_VERSION_MINOR = 0
    PRE_VICE_VERSION = 'VICE Version'   #+0x1a  VERSION_MAGIC+VERSION+SVNVERSION
    
    #see https://vice-emu.sourceforge.io/vice_9.html#SEC255
    SIZE_MAGIC = 19
    SIZE_MACHINE = 16
    SIZE_VICE_VERSION = 21 # 16+13+4

    data = []   #:array[0..18] of char;
    data_byte = 0
    version_major  = 0
    version_minor = 0
    filepos = 0

    print('snapshot header check: ')

    # check magic string...
    magic_string = _values_to_ascii(snapshot[filepos:filepos+SIZE_MAGIC-1]); filepos += SIZE_MAGIC
    print('magic_string = "%s"' %magic_string)
    if (magic_string == PRE_MAGIC) :
        print('VICE snapshot file (ok)', end='')
    else :
        print('wrong header')
        return None

    # check version...
    version_major = snapshot[filepos]; filepos += 1
    version_minor = snapshot[filepos]; filepos += 1
    print(', version "%d.%d" ' % (version_major, version_minor), end='')
    if (
        (version_major == PRE_VERSION_MAJOR) and
        (version_minor == PRE_VERSION_MINOR)
    ) :
        print('(ok)', end='');
    else :
        print('(might be unsupported: only %d.%d)' % (PRE_VERSION_MAJOR, PRE_VERSION_MINOR), end='')
        #return None

    # check machine type...
    machine = _values_to_ascii(snapshot[filepos:filepos+SIZE_MACHINE]); filepos += SIZE_MACHINE
    print(', machine: "%s" ' %machine, end='')
    if (machine == PRE_MACHINE) :
        print('(ok)', end='')
    else :
        print('(unsuported: only "%s").' % PRE_MACHINE)
        return None

    #annoying: vice 3.0.0 has a VICE Version stored now...
    tmp_pos = filepos  # store this position
    vice_version = _values_to_ascii(snapshot[filepos:filepos+SIZE_VICE_VERSION-9]); filepos += SIZE_VICE_VERSION
    print(', vice version "%s"' % vice_version, end='')
    if (vice_version == PRE_VICE_VERSION) :
        print('(given), ', end='');
    else :
        print('(not given), ', end='');
        filepos = tmp_pos  # return to position after snapshotfile-header
     
    # finish...
    print('done.')
    
    #filepos += 1
    
    return True



def _read_module() :
    global filepos
    global c64_cia2, c64_vic, c64_colram, c64_memory
    
    module_name = ''
    data_byte = 0
    module_size = 0
    bytes_read = 0
    version_major = 0
    version_minor = 0
    interesting_module = False
    
    #see https://vice-emu.sourceforge.io/vice_9.html#SEC255
    SIZE_MODULE_NAME = 16

    # read module header:

    # read module name (+16b)...
    module_name = _values_to_ascii(snapshot[filepos:filepos+SIZE_MODULE_NAME])
    print(' reading module "%s" at position %d [$%x]' %(module_name,filepos,filepos), end='')
    filepos += SIZE_MODULE_NAME

    # read version (+2b)... 
    version_major = snapshot[filepos]; filepos += 1
    version_minor = snapshot[filepos]; filepos += 1
    print(' (v%d.%d)' % (version_major, version_minor), end='')

    # read size (+4b)...
    module_size = _values_to_number(snapshot[filepos:filepos+4])
    module_size -= (SIZE_MODULE_NAME+1+1+4)   #substract header
    print(' %d [$%x] bytes' % (module_size, module_size), end='')
    filepos += 4


    # read module data:

    #C64MEM
    if (module_name == 'C64MEM') :
        #see https://vice-emu.sourceforge.io/vice_9.html#SEC268
        interesting_module = True
        print(' -> reading...', end='')
        c64_memory = snapshot[filepos+OFFSET_RAM:filepos+OFFSET_RAM+SIZE_C64_MEMORY]
        print('(%d [$%x] bytes_read),' %(SIZE_C64_MEMORY,SIZE_C64_MEMORY), end='')	# read 64k memory

    #VIC
    if (module_name == 'VIC-II') :
        interesting_module = True
        print(' -> reading...', end='')
        c64_vic = snapshot[filepos+OFFSET_VIC:filepos+OFFSET_VIC+SIZE_C64_VIC]
        print('(%d [$%x] bytes_read),' %(SIZE_C64_VIC,SIZE_C64_VIC), end='')
        c64_colram = snapshot[filepos+OFFSET_COLRAM:filepos+OFFSET_COLRAM+SIZE_C64_COLRAM]
        print('(%d [$%x] bytes_read),' %(SIZE_C64_COLRAM,SIZE_C64_COLRAM), end='')

    #CIA2
    if (module_name == 'CIA2') :
        interesting_module = True
        print(' -> reading...', end='')
        read_size = SIZE_C64_CIA2
        c64_cia2 = snapshot[filepos+OFFSET_CIA:filepos+OFFSET_CIA+SIZE_C64_CIA2]
        print('(%d [$%x] bytes_read),' %(SIZE_C64_CIA2,SIZE_C64_CIA2), end='')


    if (interesting_module == False) :
        print(' -> skipping,', end='')

    print(' done.', end='')

    filepos += module_size
    print ('')


def _write_koala(
    filename
) :
    data = []

    print(' writing koala-image ($6000):', end='')
    #load address
    print(' load address', end='')
    data.append(0x0060) #high
    data.append(0x0000) #low
    #bitmap
    print(', bitmap', end='')
    for i in range(0,8000) :
        data.append(c64_memory[addr_bitmap+i])
    #screen
    print(', screen', end='')
    for i in range(0,1000) :
        data.append(c64_memory[addr_screen+i])
    #colram
    print(', colram', end='')
    for i in range(0,1000) :
        data.append(c64_colram[i])
    #border color
    print(', background color', end='')
    data.append(value_d021)
    print(' writing done.')

    _save_some_data(filename,data)
    return None


def _write_hires(
    filename
) :
    data = []

    print(' writing hires-image ($6000):', end='')
    #load address
    print(' load address', end='')
    data.append(0x0060) #high
    data.append(0x0000) #low
    #bitmap
    print(', bitmap', end='')
    for i in range(0,8000) :
        data.append(c64_memory[addr_bitmap+i])
    #screen
    print(', screen', end='')
    for i in range(0,1000) :
        data.append(c64_memory[addr_screen+i])
    #border color
    print(', border color', end='')
    data.append(value_d020)
    print(' writing done.')
    _save_some_data(filename,data)
    return None



def _write_petscii(
    filename
) :
    data = []

    print(' writing petscii ($3000):', end='')
    #bitmap
    print(' load address', end='')
    data.append(0x0030) #high
    data.append(0x0000) #low
    #font
    if (mode_custom_font == True) :
        print(', font', end='')
        for i in range(0,0x0800) :
            data.append(c64_memory[addr_font+i])
    else :
        print(', skipping original font', end='')
    #screen
    print(', screen', end='')
    for i in range(0,1000) :
        data.append(c64_memory[addr_screen+i])
    #colram
    print(', colram', end='')
    for i in range(0,1000) :
        data.append(c64_colram[i])
    #border color
    print(', background color', end='')
    data.append(value_d021)
    print(', border color', end='')
    data.append(value_d020)
    print(' writing done.')

    _save_some_data(filename,data)

    return None





def _write_sprites(
    filename
):
    data = []
    
    print(' writing sprites:', end='')
    #load address
    print(' load address', end='')
    data.append(0x0020) #high
    data.append(0x0000) #low
    #sprite1
    print(', sprite 1', end='')
    for i in range(0,63) :
        data.append(c64_memory[value_sprite1_memory+i])
    data.append(0)
    #sprite2
    print(', sprite 2', end='')
    for i in range(0,63) :
        data.append(c64_memory[value_sprite2_memory+i])
    data.append(0)
    #sprite3
    print(', sprite 3', end='')
    for i in range(0,63) :
        data.append(c64_memory[value_sprite3_memory+i])
    data.append(0)
    #sprite4
    print(', sprite 4', end='')
    for i in range(0,63) :
        data.append(c64_memory[value_sprite4_memory+i])
    data.append(0)
    #sprite5
    print(', sprite 5', end='')
    for i in range(0,63) :
        data.append(c64_memory[value_sprite5_memory+i])
    data.append(0)
    #sprite6
    print(', sprite 6', end='')
    for i in range(0,63) :
        data.append(c64_memory[value_sprite6_memory+i])
    data.append(0)
    #sprite7
    print(', sprite 7', end='')
    for i in range(0,63) :
        data.append(c64_memory[value_sprite7_memory+i])
    data.append(0)
    #sprite8
    print(', sprite 8', end='')
    for i in range(0,63) :
        data.append(c64_memory[value_sprite8_memory+i])
    data.append(0)

    print(' writing done.')

    _save_some_data(filename,data)

    return None


def _do_it(
    args
) :
    global snapshot
    global filepos
    
    snapshot = _load_some_data(args.snapshot)
    
    if ( _check_snapshot_header() ) :
        print('header checks passed.')
    else :
        print('header checks failed.')
        return None
    
    while (filepos < len(snapshot)) :
        _read_module()        
    #breakpoint()
    
    _process()


    # koala
    if (
        (mode_bitmap == True) &
        (mode_multicolor == True)
    ) : _write_koala(args.output+'-koala.kla')

    # hires
    if (
        (mode_bitmap == True) &
        (mode_multicolor == False)
    ) : _write_hires(args.output+'-hires.hir')

    # petscii
    if (
        (mode_bitmap == False)
    ) : _write_petscii(args.output+'-petscii.bin')

    _write_sprites(args.output+'-spriteset.spr')

    return None



def _get_parser(
) :
    #https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description='This script parses C64 Vice snapshots and extracts koala or hires images, sprites, font and petscii from it.',
        epilog='Example: ./snaprip.py snapshot.vsf test'
    )
    parser.add_argument('snapshot', help='snapshot file')
    parser.add_argument('output', help='output filename')

    return parser



def _main_procedure() :
    print("%s v%s [%s] *** by fieserWolF"% (PROGNAME, VERSION, DATUM))

    parser = _get_parser()
    args = parser.parse_args()

    _do_it(args)


if __name__ == '__main__':
    _main_procedure()

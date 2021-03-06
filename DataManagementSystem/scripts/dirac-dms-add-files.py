#!/usr/bin/env python
########################################################################
# $HeadURL$
# File :    dirac-dms-add-file
# Author :  Stuart Paterson
########################################################################
"""
  Upload a file to the grid storage and register it in the File Catalog
"""
__RCSID__ = "$Id$"

from DIRAC.Core.Base import Script
import os
Script.setUsageMessage( '\n'.join( [ __doc__.split( '\n' )[1],
                                     'Usage:',
                                     '  %s [option|cfgfile] ... LFN Path SE [GUID]' % Script.scriptName,
                                     'Arguments:',
                                     '  LFN:      Logical File Name',
                                     '  Path:     Local path to the file',
                                     '  SE:       DIRAC Storage Element',
                                     '  GUID:     GUID to use in the registration (optional)' ,
                                     ' ++ OR ++',
                                     'Usage:',
                                     '  %s [option|cfgfile] ... LocalFile' % Script.scriptName,
                                     'Arguments:',
                                     '  LocalFile: Path to local file containing all the above, i.e.:',
                                     '  lfn1 localfile1 SE [GUID1]',
                                     '  lfn2 localfile2 SE [GUID2]'] )
                        )

Script.parseCommandLine( ignoreErrors = True )
args = Script.getPositionalArgs()
if len( args ) < 1 or len( args ) > 4:
  Script.showHelp()

def getDict(item_list):
  """
    From the input list, populate the dictionary
  """
  lfn_dict = {}
  lfn_dict['lfn'] = item_list[0]
  lfn_dict['localfile'] = item_list[1]
  lfn_dict['SE'] = item_list[2]
  guid = None
  if len( item_list ) > 3:
    guid = item_list[3]
  lfn_dict['guid'] = guid
  return lfn_dict
  
lfns = []
if len(args)==1:
  inputFileName = args[0]
  if os.path.exists( inputFileName ):
    inputFile = open( inputFileName, 'r' )
    for line in inputFile:
        line = line.rstrip()
        items = line.split()
        lfns.append(getDict(items))
    inputFile.close()
else:
  lfns.append(getDict(args))
  
from DIRAC.DataManagementSystem.Client.ReplicaManager import ReplicaManager
from DIRAC import gLogger
import DIRAC
exitCode = 0

rm = ReplicaManager()
for lfn in lfns:
  if not os.path.exists( lfn['localfile'] ):
    gLogger.error("File %s must exist locally"%lfn['localfile'])
    exitCode = 1
    continue
  if not os.path.isfile( lfn['localfile'] ):
    gLogger.error("%s is not a file"%lfn['localfile'])
    exitCode = 2
    continue

  gLogger.info("\nUploading %s"%lfn['lfn'])
  res = rm.putAndRegister(lfn['lfn'],lfn['localfile'],lfn['SE'],lfn['guid'])
  if not res['OK']:
    exitCode = 3
    continue

DIRAC.exit( exitCode )

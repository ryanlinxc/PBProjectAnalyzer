#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import re
import hashlib
import uuid
import weakref
from PBXProjectHelper import PBXProjectHelper

def printInvalidSet(prefix, invalidSet):
    for g in invalidSet:
        print prefix + g

def findTopParent(groupDic, nodeId):
    topParentId = nodeId
    while(1):
        parentDic = {k: v for k, v in groupDic.iteritems() if topParentId in v['children'] }
    
        if len(parentDic) == 0:
            break
        else:
            topParentId = next(iter(parentDic))
    return topParentId

helper = PBXProjectHelper ("/Users/linxiaocheng/Downloads/Test/Test.xcodeproj/project.pbxproj")
objects = helper.root['objects']

# check group : 引用链 PBXGroup —>其它PBXGroup —-> PBXProject(mainGroup)
groupDic = {k: v for k, v in objects.iteritems() if v['isa'] == 'PBXGroup' }
topParentId = '1664C306216B655A00BE8F50'
validGroupDic = dict()
for objId, objData in groupDic.iteritems():
    if findTopParent(groupDic, objId) != topParentId:
        print 'PBXGroup，可能多余: ' + objId
    else:
        validGroupDic[objId] = objData

# check build file : 引用链：PBXBuildFile —> PBXSourcesBuildPhase\PBXFrameworksBuildPhase\PBXResourcesBuildPhase —> PBXNativeTarget —>  PBXProject
allBuildFileDic = {k: v for k, v in objects.iteritems() if v['isa']  == 'PBXBuildFile'}
buildFileInTreeDic = dict()

for objId, objData in objects.iteritems():
    if objData['isa'] == 'PBXProject':
        for targetId in objData['targets']:
            if targetId in objects:
                for buildPhaseId in objects[targetId]['buildPhases']:
                    if buildPhaseId in objects:
                            for buildFileId in objects[buildPhaseId]['files']:
                                if buildFileId in objects:
                                    buildFileInTreeDic[buildFileId] = objects[buildFileId]

printInvalidSet("PBXBuildFile，可能多余： ", set(allBuildFileDic.keys()).difference(set(buildFileInTreeDic.keys())))

# check header file: 引用链： PBXFileReference —> PBXGroup —>其它PBXGroup —-> PBXProject(mainGroup) 
allFilePrefDic = {k: v for k, v in objects.iteritems() if v['isa']  == 'PBXFileReference'}
filePrefInValidGroupDic = dict();
filePrefInValidBuildDic = dict();
for objId, objData in validGroupDic.iteritems():
    for child in objData['children']:
        if child in objects:
            childData = objects[child]
            if childData['isa'] == 'PBXFileReference':
                filePrefInValidGroupDic[child] = childData

for objId, objData in buildFileInTreeDic.iteritems():
    filePrefId = objData['fileRef']
    if filePrefId in objects:
        filePrefData = objects[filePrefId]
        if filePrefData['isa'] == 'PBXFileReference':
            filePrefInValidBuildDic[filePrefId] = filePrefData


for filePrefId, filePrefData in allFilePrefDic.iteritems():
    filename, file_extension = os.path.splitext(filePrefData['path'])
    if file_extension == '.h':
        if filePrefId not in filePrefInValidGroupDic:
            print 'PBXFileReference，可能多余： ' + filePrefId
    elif file_extension == '.m':
        invalid = False
        if filePrefId not in filePrefInValidGroupDic:
            invalid = True
        if filePrefId not in filePrefInValidBuildDic:
            invalid = True
        if invalid:
            print 'PBXFileReference，可能多余： ' + filePrefId
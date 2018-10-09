整理：PBXFileReference、PBXBuildFile、PBXGroup，输出多余的id

1. .h、.m文件引用链：PBXFileReference —> PBXGroup —>其它PBXGroup —-> PBXProject(mainGroup) —> 根属性：1664C307216B655A00BE8F50
2. .m文件额外引用链：PBXFileReference —> PBXBuildFile —-> PBXSourcesBuildPhase —> PBXNativeTarget —>  PBXProject —> 根属性：1664C307216B655A00BE8F50
3. Buildfile: PBXBuildFile —> PBXSourcesBuildPhase —> PBXNativeTarget —>  PBXProject

$ErrorActionPreference = 'Stop'
Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
public class AudioLockQuery {
  [StructLayout(LayoutKind.Sequential)] public struct FILETIME { public uint low; public uint high; }
  [StructLayout(LayoutKind.Sequential)] public struct UNIQUE_PROCESS { public int pid; public FILETIME start; }
  [StructLayout(LayoutKind.Sequential, CharSet=CharSet.Unicode)] public struct PROCESS_INFO {
    public UNIQUE_PROCESS process;
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst=256)] public string appName;
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst=64)] public string service;
    public uint appType; public uint status; public uint session; [MarshalAs(UnmanagedType.Bool)] public bool restartable;
  }
  [DllImport("rstrtmgr.dll", CharSet=CharSet.Unicode)] static extern int RmStartSession(out uint handle, int flags, string key);
  [DllImport("rstrtmgr.dll", CharSet=CharSet.Unicode)] static extern int RmRegisterResources(uint handle, uint files, string[] paths, uint apps, IntPtr processes, uint services, string[] names);
  [DllImport("rstrtmgr.dll")] static extern int RmGetList(uint handle, out uint needed, ref uint count, [In,Out] PROCESS_INFO[] info, ref uint reasons);
  [DllImport("rstrtmgr.dll")] static extern int RmEndSession(uint handle);
  public static PROCESS_INFO[] Query(string path) {
    uint handle; int result=RmStartSession(out handle,0,Guid.NewGuid().ToString("N"));
    if(result!=0) throw new Exception("RmStartSession: "+result);
    try {
      result=RmRegisterResources(handle,1,new string[]{path},0,IntPtr.Zero,0,null);
      if(result!=0) throw new Exception("RmRegisterResources: "+result);
      uint needed=0,count=0,reasons=0; result=RmGetList(handle,out needed,ref count,null,ref reasons);
      if(result==0) return new PROCESS_INFO[0];
      if(result!=234) throw new Exception("RmGetList: "+result);
      var info=new PROCESS_INFO[needed]; count=needed;
      result=RmGetList(handle,out needed,ref count,info,ref reasons);
      if(result!=0) throw new Exception("RmGetList: "+result);
      Array.Resize(ref info,(int)count); return info;
    } finally { RmEndSession(handle); }
  }
}
'@
$taskPath = Join-Path (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../..')).Path "Help! I'm not just AI - Final.mp3"
[AudioLockQuery]::Query($taskPath) | ForEach-Object {
  $taskPid=$_.process.pid
  $taskProcess=Get-CimInstance Win32_Process -Filter "ProcessId=$taskPid"
  [pscustomobject]@{pid=$taskPid; app=$_.appName; executable=$taskProcess.ExecutablePath; commandLine=$taskProcess.CommandLine}
} | ConvertTo-Json -Depth 4

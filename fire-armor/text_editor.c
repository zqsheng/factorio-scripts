#include <stdlib.h>

typedef struct node_s {
	char *value;
	int cnt;
	struct node_s *prev, *next;
} node_t;

typedef struct {
	node_t root;
} TextEditor;


TextEditor* textEditorCreate() {
	TextEditor *te = (TextEditor *) malloc(sizeof(TextEditor));
	te->root = NULL;
	return te;
}

void textEditorAddText(TextEditor* obj, char* text) {
	    
}

int textEditorDeleteText(TextEditor* obj, int k) {
	    
}

char* textEditorCursorLeft(TextEditor* obj, int k) {
	    
}

char* textEditorCursorRight(TextEditor* obj, int k) {
	    
}

void textEditorFree(TextEditor* obj) {
	    
}


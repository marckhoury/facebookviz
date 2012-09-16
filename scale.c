/*
 * Written by Marc Khoury
 */
#include <stdio.h>
#include <stdlib.h>
#include <graphviz/cgraph.h>

char* pos_to_str(double x, double y)
{
	char buffer[256];
	char* s;
	int i,length;
	length = sprintf(buffer, "%lf, %lf", x, y);
	s = (char*) malloc(sizeof(char)*(length+1));
	for(i = 0; i < length; i++) {
		s[i] = buffer[i];
	}
	s[length] = '\0';
	return s;
}

void usage()
{
	printf("Usage: scale <scale> <infile>\n");
	exit(1);
}

int main(int argc, char* argv[])
{
	if(argc != 3)
		usage();
	float scale = atof(argv[1]);
	FILE* fin = fopen(argv[2],"r");
	Agraph_t* g = agread(fin, (Agdisc_t*)NULL);
	Agnode_t* n;
	
	for(n = agfstnode(g); n; n = agnxtnode(g,n)) {
		char* pos = agget(n,"pos");
		double x,y;
		sscanf(pos,"%lf,%lf",&x,&y);
		x *= scale;
		y *= scale;		
		char* s = pos_to_str(x,y);
		agset(n,"pos",s);
		free(s);
	}
	
	agwrite(g,stdout);
	
	agclose(g);
	return 0;
}

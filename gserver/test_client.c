#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <netdb.h>
#include <unistd.h>
#include <time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/time.h>

#define COLOR_LEN 30
#define DEF_PORT 12345
#define DEF_MSG_SIZE 100
#define BUF_SIZE 10000

void Send (int, char *);

/*
 * This program is simple test of the operation of the game server, which takes text lines terminated by carriage returns
 * from each of two players and relays the moves between them.
 */

void Usage(char *prog)
{
	printf ("Usage: %s %s\n", prog, "[-c color] [-p port] serverhost");
	exit(0);
}

int main (int argc, char *argv[]) {
  extern char *optarg;
  extern int optind, opterr;
  int sock;
  in_addr_t interface_addr = htonl(INADDR_ANY);
  struct sockaddr_in name;
  struct hostent *hp, *gethostbyname(const char *);
  int c, op;
  char buf[BUF_SIZE];
  char *serverIP;
  int serverPort = DEF_PORT;
  char color[COLOR_LEN];
  char moves[] = "NSEW";
  //char moves[] = "DLR";

  strcpy (color, "white");

  /* check command line arguments */
  while ((c = getopt(argc, argv, "c:i:p:")) != -1) {
    switch (c) {
    case 'c':
      strcpy (color, optarg);
      break;
     case 'p':
  	serverPort = atoi(optarg);
	break;
    default:
      Usage(argv[0]);
    }
  }

  if (optind >= argc) {
      Usage(argv[0]);
  }

  serverIP = argv[optind];

  /* Create socket on which to send. */
  sock = socket(AF_INET, SOCK_STREAM, 0);
  if (sock < 0) {
    perror("opening socket");
    exit(1);
  }

  name.sin_family = AF_INET;
  name.sin_port = htons(serverPort);

  if ((hp = gethostbyname(serverIP)) == 0) {
    fprintf (stderr, "unknown host: %s\n", serverIP);
    exit(1);
  }
  memcpy(&name.sin_addr, hp->h_addr, hp->h_length);

  fprintf (stderr, "Connecting to %s on port %d (TCP)\n", 
	   serverIP, serverPort);
  if (connect(sock, (struct sockaddr *)&name, sizeof(name)) < 0) {
    perror("connecting stream socket");
    exit(1);
  }

  /* initialize the random number seed */
  srand(time(NULL)); 

  /* now run through a pretend game sequence */
  sprintf (buf, "%s %s\n", "mytestgame", color);
  Send(sock, buf);

  while (1) {
    sleep(1);
    /*
     * for games involving movement of a single piece:
     * generate a random move, consisting of two digits a cardinal direction, and another digit 
     * sprintf (buf, "%d%d%c%d\n", rand() % 7 + 1, rand() % 7  + 1,  moves[rand() % 3], rand() % 3 + 1);
     */
    
    /*
     * for games involving dropping or sliding of pieces:
     * generate a random move, consisting of two digits a cardinal direction, and another digit 
     */
    op = moves[rand() % 2];
    // if (op == 'D')
    //  sprintf (buf, "%c %d\n", op, rand() % 8 + 1);
    // else
    //  sprintf (buf, "%c %d %d\n", op, rand() % 8 + 1, rand() % 8  + 1);
    sprintf (buf, "%d%d%c%d\n", rand() % 7 + 1, rand() % 7  + 1, op,  rand() % 3  + 1);

    Send(sock, buf);
  }
  return (0);
}

void Send(int s, char *b) {
  int nread;

  write (s, b, strlen(b));
  if ((nread = read(s, b, BUF_SIZE)) < 0) {
    perror("reading from socket");
    exit (1);
  }
  if (strchr(b, '\n')) strtok(b, "\n");  /* purge carriage return if provided */
  printf ("read %s\n", b);
}



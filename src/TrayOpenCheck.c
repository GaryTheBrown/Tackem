#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/cdrom.h>

int main(int argc,char **argv) {
	int cdrom;
	int status=0;

	if (! argv[1] ){
		printf("Usage : trayopen [device]\n");
		printf("Result: Returns a 0 if the tray was open and 1 if it was closed\n");
		exit(2);
	}

	if ((cdrom = open(argv[1],O_RDONLY | O_NONBLOCK)) < 0) {
		printf("Unable to open device %s. Provide a device name (/dev/sr0, /dev/cdrom) as a parameter.\n",argv[1]);
		exit(2);
	}
	/* Check CD tray status */
	if (ioctl(cdrom,CDROM_DRIVE_STATUS) == CDS_TRAY_OPEN) {
		status=1;
	}

	close(cdrom);
	exit(status);
}

//https://askubuntu.com/questions/226638/how-to-eject-a-cd-dvd-from-the-command-line
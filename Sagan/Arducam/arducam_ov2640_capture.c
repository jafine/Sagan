/*-----------------------------------------

//Update History:
//2016/06/13 	V1.1	by Lee	add support for burst mode

--------------------------------------*/
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <wiringPiSPI.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <pwd.h>
#include <grp.h>
#include "arducam.h"
#define OV2640_CHIPID_HIGH  0x0A
#define OV2640_CHIPID_LOW   0x0B

#define BUF_SIZE (384*1024)
uint8_t buffer[BUF_SIZE] = {0xFF};
void setup()
{
    uint8_t vid,pid;
    uint8_t temp;
    wiring_init();
    arducam(smOV2640,CAM1_CS,-1,-1,-1);
    
     // Check if the ArduCAM SPI bus is OK
    arducam_write_reg(ARDUCHIP_TEST1, 0x55, CAM1_CS);
    temp = arducam_read_reg(ARDUCHIP_TEST1, CAM1_CS);
    //printf("temp=%x\n",temp);
    if(temp != 0x55) {
        printf("SPI interface error!\n");
        exit(EXIT_FAILURE);
    }
     else{
    	   //printf("SPI interface OK!\n");
    	}
    
    // Change MCU mode
    arducam_write_reg(ARDUCHIP_MODE, 0x00, CAM1_CS);
    
    // Check if the camera module type is OV2640
    arducam_i2c_read(OV2640_CHIPID_HIGH, &vid);
    arducam_i2c_read(OV2640_CHIPID_LOW, &pid);
    if((vid != 0x26) || (pid != 0x42)) {
        printf("Can't find OV2640 module!\n");
        exit(EXIT_FAILURE);
    } else {
        //printf("OV2640 detected\n");
    }
}

int main(int argc, char *argv[])
{
    if (argc == 1)
    {
        printf("Usage: %s [-s <resolution>] | [-c <filename]", argv[0]);
        printf(" -s <resolution> Set resolution, valid resolutions are:\n");
        printf("                   160x120\n");
        printf("                   176x144\n");
        printf("                   320x240\n");
        printf("                   352x288\n");
        printf("                   640x480\n");
        printf("                   800x600\n");
        printf("                   1024x768\n");
        printf("                   1280x1024\n");
        printf("                   1600x1200\n");
        printf(" -c <filename>   Capture image\n");
        exit(EXIT_SUCCESS);
    }

  	if (strcmp(argv[1], "-c") == 0 && argc == 4) 
  	{
      setup();
      arducam_set_format(fmtJPEG);
      arducam_init();
      // Change to JPEG capture mode and initialize the OV2640 module   
      if (strcmp(argv[3], "160x120") == 0) arducam_set_jpeg_size(sz160x120);
      else if (strcmp(argv[3], "176x144") == 0) arducam_set_jpeg_size(sz176x144);
      else if (strcmp(argv[3], "320x240") == 0) arducam_set_jpeg_size(sz320x240);
      else if (strcmp(argv[3], "352x288") == 0) arducam_set_jpeg_size(sz352x288);
      else if (strcmp(argv[3], "640x480") == 0) arducam_set_jpeg_size(sz640x480);
      else if (strcmp(argv[3], "800x600") == 0) arducam_set_jpeg_size(sz800x600);
      else if (strcmp(argv[3], "1024x768") == 0) arducam_set_jpeg_size(sz1024x768);
      else if (strcmp(argv[3], "1280x960") == 0) arducam_set_jpeg_size(sz1280x960);
      else if (strcmp(argv[3], "1600x1200") == 0) arducam_set_jpeg_size(sz1600x1200);
      else {
      printf("Unknown resolution %s\n", argv[3]);
      exit(EXIT_FAILURE);
      }
      sleep(1); // Let auto exposure do it's thing after changing image settings
      //printf("Changed resolution1 to %s\n", argv[3]);
      //delay(1000);
      
      // Flush the FIFO
      arducam_flush_fifo(CAM1_CS);    
      // Clear the capture done flag
      arducam_clear_fifo_flag(CAM1_CS);
      // Start capture
      //printf("Start capture\n");  
      arducam_start_capture(CAM1_CS);
      while (!(arducam_read_reg(ARDUCHIP_TRIG,CAM1_CS) & CAP_DONE_MASK)) ;
      //printf("CAM1 Capture Done\n");
              
       // Open the new file
      FILE *fp1 = fopen(argv[2], "w+");

      if (!fp1) {
          printf("Error: could not open %s\n", argv[2]);
          exit(EXIT_FAILURE);
      }
       
      //printf("Reading FIFO\n");    
      /**NEW CODE**/
	/*size_t len = read_fifo_length(CAM1_CS);
      if (len >= 393216){
	printf("Over size.");
	exit(EXIT_FAILURE);
      }else if (len == 0 ){
	printf("Size is 0.");
	exit(EXIT_FAILURE);
      }
      digitalWrite(CAM1_CS,LOW);  //Set CS low       
      set_fifo_burst(BURST_FIFO_READ);
      arducam_spi_transfers(buffer,1);//dummy read  
      int32_t i=0;
      while(len>4096)
      {	 
      	arducam_transfers(&buffer[i],4096);
      	len -= 4096;
      	i += 4096;
      }
      arducam_spi_transfers(&buffer[i],len); 

      fwrite(buffer, len+i, 1, fp1);
      digitalWrite(CAM1_CS,HIGH);  //Set CS HIGH
       //Close the file
      delay(100);
	*/
	/**OLD CODE**/
	uint8_t temp, temp_last;
	uint8_t buf[256];
	int i = 0;
	int nmemb = 1;
	temp = arducam_read_fifo(CAM1_CS);

	//Write first image data to buffer
	buf[i++] = temp;

	//Read JPEG data from FIFO
	while( (temp != 0xD9) | (temp_last != 0xFF) )
    {
	temp_last = temp;
	temp = arducam_read_fifo(CAM1_CS);

	//Write image data to buffer if not full
	if(i < 256)
		buf[i++] = temp;
	else
	{
		//Write 256 uint8_ts image data to file
		fwrite(buf,256,nmemb,fp1);
		
		i = 0;
			buf[i++] = temp;
		}
	}
	//Write the remain uint8_ts in the buffer
	if(i > 0)
	fwrite(buf,i,nmemb,fp1);

	fclose(fp1);
      
	struct passwd *pwd;
	struct group *grp;

	const char name[3] = "pi";
	pwd = getpwnam(name);
	grp = getgrnam(name);

	chown(argv[2], pwd->pw_uid, grp->gr_gid);
	// Clear the capture done flag
      arducam_clear_fifo_flag(CAM1_CS);
	
  } else {
      printf("Error: unknown or missing argument.\n");
	int i;
	printf("Number of arguments [argc]: %d\n", argc);
	for(i = 0; i < argc; ++i){
		printf("Argument %d: %s\n", i, argv[i]);
	}
      exit(EXIT_FAILURE);
  }
  exit(EXIT_SUCCESS);
}

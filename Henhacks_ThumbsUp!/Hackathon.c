#include <stdio.h>
#include <stdlib.h>

int main(void) {
    //char *url = "https://github.com/OpenGenus/cosmos/archive/refs/heads/master.zip";
    char *url = "https://github.com/mada028/Hackathon/archive/refs/heads/main.zip";
    char *filepath = "D:\\HelpfulResources\\bruh.zip";
    char *extraction_path = ":\\HelpfulResources\\Resources";
    char command[1024];
    FILE *fp;

    // create command string to download file
    sprintf(command, "powershell -Command \"(new-object System.Net.WebClient).DownloadFile('%s','%s')\"", url, filepath);

    // execute command to download the zip file
    if (system(command) == -1) {
        printf("Failed to execute command\n");
        return 1;
    }

    // open the zip file to verify it exists
    fp = fopen(filepath, "rb");
    if (fp == NULL) {
        printf("Failed to create file\n");
        return 1;
    }
    fclose(fp);

    // create command string to extract the zip file
    sprintf(command, "powershell -Command \"Add-Type -AssemblyName System.IO.Compression.FileSystem;"
                     "[System.IO.Compression.ZipFile]::ExtractToDirectory('%s', '%s')\"", filepath, extraction_path);

    // execute command to extract the zip file
    if (system(command) == -1) {
        printf("Failed to execute command\n");
        return 1;
    }

    printf("Folder downloaded and extracted successfully\n");
    remove(filepath);

    return 0;
}

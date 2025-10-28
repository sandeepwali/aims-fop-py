# AIMS FOP Python Wrapper

AIMS FOP Python Wrapper is a script designed to interface with the Apache FOP Library. It provides multi-threaded image generation capabilities, utilizing XSLT and XML files. To ensure smooth operations, users are required to have OpenJDK 17 installed, and the XML and XSLT files should be appropriately placed in the input directory.

## Prerequisites

OpenJDK 17:
* You must have OpenJDK 17 installed on your machine.
* For easy installation, you can download OpenJDK 17 from Microsoft's official website: [OpenJDK 17 Download](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-17).

## How to Use

1. Organize Your Files:
    * Place your XML and XSLT files in the structure: `input/<folder_name>/*`.
    * Each folder under input can have multiple XSLT and XML files.

2. Run the Script:
    * Simply execute the `main.py` script to start the image generation process. This will generate images based on the provided XSLT and XML files and place them in the output directory.

## Notes

* Ensure that Java's bin directory (containing the java.exe executable) is added to your system's PATH environment variable. This ensures that the script can invoke Java without issues.
* The generated images are based on the transformations specified in your XSLT files applied to your XML files. Ensure your XSLT is correctly defined for accurate image generation.

## Contributing

For any improvements or issues, please refer to our [GitLab repository](https://gitlab.solumesl.com/solum-esl/utils/aims-4-py-utils).

## License

This project is licensed under the MIT/X11 License. See the [LICENSE](LICENSE) file for more details.

## Contact

If you have any questions or need assistance, you can reach out to the project maintainers via seg-ae@solumesl.com or glenn.goffin@solumesl.com.

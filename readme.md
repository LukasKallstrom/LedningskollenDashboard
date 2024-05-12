
# Dash Application

## Overview
This repository contains a Dash application designed to search and process data from an Excel file named "Ledningsägare.xlsx". The application specifically looks for data in the row labeled "Omsättning (tkr)" and provides a user-friendly interface to visualize and interact with this data, aswell as downloading an excel of the filtered data (currently downloads all the data for the selected companies, not only the selected columns).

All company names were collected from "[https://www.ledningskollen.se/Vilka-ar-med_](https://www.ledningskollen.se/Vilka-ar-med_)" and all revenue data was collected from "[Allabolag.se](https://www.allabolag.se/)", websites and data open to the public.

## Getting Started

### Prerequisites
Before running the application, ensure you have Docker installed on your machine. Visit [Docker's official website](https://www.docker.com/get-started) for installation instructions.

### Running the Application

1. **Build the Docker Image**

   Use the following command to build the Docker image for the Dash application:

   ```
   docker build -t dash-app .
   ```

2. **Run the Application**

   After building the image, run the application using the following command:

   ```
   docker run -p 4093:4093 dash-app
   ```

   This command will start the application and make it accessible at `http://localhost:4093`
   (feel free to change the port, but remember to change the port in both the dockerfile aswell as in this command)

## Creating an Executable with PyInstaller

To create an executable for your application, you'll need to use PyInstaller. Follow these steps to setup and build the executable:

### Prerequisites
Ensure you have PyInstaller installed. If not, you can install it using pip:

```bash
pip install pyinstaller
```

### Building the Executable

1. **Prepare your files:**
   - Ensure you have the `app.py` script in your working directory.
   - Make sure that an Excel file named `Ledningsägare.xlsx` is present in the same directory as your script. This file is necessary for the executable to function properly.

2. **Generate the executable:**
   - Run the following command in your terminal or command prompt:

```bash
pyinstaller --onefile --add-data "Ledningsägare.xlsx;." app.py
```

   - This command tells PyInstaller to bundle everything into a single executable file including the `Ledningsägare.xlsx` file. The resulting file `app.exe` will be located in the `dist` folder within your current directory.

### Running the Executable

- After building, you can run `app.exe` directly from the `dist` folder as long as the `Ledningsägare.xlsx` file is in the same folder as the executable.


## Features
- **Excel Data Processing**: The app is capable of reading the "Ledningsägare.xlsx" file to analyze and display relevant financial data.
- **Interactive Dashboards**: Users can interact with visualizations to better understand the data.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

